# -*- coding: utf-8 -*-
import os
from django.db import models
from django.contrib.auth.models import User
from thumbs import ImageWithThumbsField

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
        return os.path.join('albums', str(self.id))

    def save(self, *args, **kwargs):
        super(Album,self).save()
        if not os.path.exists(self.path()):
            os.makedirs(self.path())

def pin_path(instance,filename):
    return instance.path(filename)

class Pin(models.Model):
    album = models.ForeignKey(Album)
    image = ImageWithThumbsField('照片',upload_to=pin_path, sizes=((200, 1000),))
    description = models.TextField('描述',blank=True, null=True)

    def __unicode__(self):
        return self.image.name

    def path(self,filename):
        return os.path.join(self.album.path(),filename)

    def save(self, *args, **kwargs):
        '''
        if not self.image:
            temp_img = NamedTemporaryFile()
            temp_img.write(urllib2.urlopen(self.url).read())
            temp_img.flush()
            # pylint: disable-msg=E1101
            self.image.save(self.url.split('/')[-1], File(temp_img))
            '''
        super(Pin, self).save()

    class Meta:
        ordering = ['-id']
