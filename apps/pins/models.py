# -*- coding: utf-8 -*-
import os
import shutil
from django.db import models
from django.contrib.auth.models import User
from django.conf import settings
from django.utils.translation import ugettext_lazy as _
from thumbs import ImageWithThumbsField

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
        return ('recent-pins', [self.id])

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

def pin_upload_to(instance,filename):
    # the disk path relative to media root
    return os.path.join(ALBUMS_DIR,str(instance.album.id),filename)

class Pin(models.Model):
    album = models.ForeignKey(Album)
    file = ImageWithThumbsField('照片',upload_to=pin_upload_to, sizes=((200, 1000),))
    description = models.TextField('描述',blank=True, null=True)

    def __unicode__(self):
        return self.file.name

    def path(self):
        return os.path.join(settings.MEDIA_ROOT,self.file.name)

    def delete(self, *args, **kwargs):
        self.file.delete()
        super(Pin,self).delete()

    class Meta:
        ordering = ['id']


class Comment((models.Model)):
    comment = models.TextField(u'评论', max_length=COMMENT_MAX_LENGTH)
    user        = models.ForeignKey(User)
    pin         = models.ForeignKey(Pin)
    submit_at = models.DateTimeField(auto_now=True)
    is_removed  = models.BooleanField(default=False)

    class Meta:
        ordering = ('submit_at',)

    def __unicode__(self):
        return "%s: %s..." % (self.name, self.comment[:50])

