import os
from django.db import models
from django.contrib.auth.models import User
from django.conf import settings
from django.core.files import File
from django.core.files.temp import NamedTemporaryFile

from thumbs import ImageWithThumbsField

import urllib2


class Album(models.Model):
    name = models.CharField(max_length=255, unique=True)
    create = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User)

    def __unicode__(self):
        return self.name

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
    image = ImageWithThumbsField(upload_to=pin_path, sizes=((200, 1000),))
    description = models.TextField(blank=True, null=True)

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
