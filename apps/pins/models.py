# -*- coding: utf-8 -*-
import os
from django.db import models
from django.contrib.auth.models import User
from django.core.files import File
from django.core.files.temp import NamedTemporaryFile
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
    file = ImageWithThumbsField('照片',upload_to=pin_path, sizes=((200, 1000),))
    description = models.TextField('描述',blank=True, null=True)

    def __unicode__(self):
        return self.file.name

    def path(self,filename):
        return os.path.join(self.album.path(),filename)

    class Meta:
        ordering = ['-id']
