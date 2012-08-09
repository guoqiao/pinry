# -*- coding: utf-8 -*-
import os
import shutil
from django.db import models
from django.contrib.auth.models import User
from django.conf import settings
from django.utils.translation import ugettext_lazy as _
from thumbs import ImageWithThumbsField,generate_thumb

COMMENT_MAX_LENGTH = getattr(settings,'COMMENT_MAX_LENGTH',3000)

ALBUMS_DIR = 'albums'

class Album(models.Model):
    name = models.CharField(u'名称', max_length=255, unique=True)
    create = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User)

    class Meta:
        ordering = ['-create']

    def __unicode__(self):
        return self.name

    @models.permalink
    def get_absolute_url(self):
        return ('album:home', [str(self.pk)])

    def path(self):
        return os.path.join(settings.MEDIA_ROOT, ALBUMS_DIR, str(self.id))

    def save(self, *args, **kwargs):
        super(Album,self).save()
        if not os.path.exists(self.path()):
            os.makedirs(self.path())

    def delete(self, *args, **kwargs):
        path = self.path()
        if os.path.exists(path):
            shutil.rmtree(path)
        super(Album,self).delete()

    def face(self):
        pins = self.pin_set.all()
        if pins:
            import random
            i = random.randint(0, len(pins)-1)
            return pins[i].file.url_200x1000
        else:
            return os.path.join(settings.STATIC_URL, 'album.png')

    def comments(self):
        return Comment.objects.filter(pin__album=self)

def pin_upload_to(instance,filename):
    # the disk path relative to media root
    return os.path.join(ALBUMS_DIR,str(instance.album.id),filename)

def _rotate(path, angle):
    import Image
    img0 = Image.open(path)
    img1 = img0.rotate(angle)
    img1.save(path)

class Pin(models.Model):
    album = models.ForeignKey(Album)
    file = ImageWithThumbsField('照片',upload_to=pin_upload_to, sizes=((200, 1000),))
    description = models.TextField('描述',blank=True, null=True)

    def __unicode__(self):
        return self.file.name

    @models.permalink
    def get_absolute_url(self):
        return ('pin:home', [str(self.pk)])

    def path(self):
        return os.path.join(settings.MEDIA_ROOT,self.file.name)

    def delete(self, *args, **kwargs):
        self.file.delete()
        super(Pin,self).delete()

    def rotate(self, angle):
        image_field = self.file
        _rotate(self.path(), angle)

        name = self.path()
        content = open(self.path())
        if image_field.sizes:
            for size in image_field.sizes:
                (w,h) = size
                split = name.rsplit('.',1)
                thumb_name = '%s.%sx%s.%s' % (split[0],w,h,split[1])
                # you can use another thumbnailing function if you like
                thumb_content = generate_thumb(content, size, split[1])
                if os.path.exists(thumb_name):
                    print 'rm', thumb_name
                    os.remove(thumb_name)
                image_field.storage.save(thumb_name, thumb_content)

    class Meta:
        ordering = ['id']


class Comment((models.Model)):
    comment = models.TextField(u'评论', max_length=COMMENT_MAX_LENGTH)
    user        = models.ForeignKey(User)
    pin         = models.ForeignKey(Pin)
    submit_at = models.DateTimeField(auto_now=True)
    is_removed  = models.BooleanField(default=False)

    class Meta:
        ordering = ('-submit_at',)

    def __unicode__(self):
        return "%s: %s..." % (self.name, self.comment[:50])

