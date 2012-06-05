import os
from django.db import models
from django.conf import settings
from django.core.files import File
from django.core.files.temp import NamedTemporaryFile

from thumbs import ImageWithThumbsField

import urllib2


class Album(models.Model):
    name = models.CharField(max_length=255)

    def __unicode__(self):
        return self.name

    def path(self):
        return os.path.join(settings.PINS_ROOT, self.name)

    def save(self, *args, **kwargs):
        if not os.path.exists(self.path()):
            os.mkdir(self.path())
        super(Album,self).save()

class Pin(models.Model):
    #album = models.ForeignKey(Album)
    #url = models.CharField(max_length=511)
    image = ImageWithThumbsField(upload_to='pins/pin', sizes=((200, 1000),))
    description = models.TextField(blank=True, null=True)

    def __unicode__(self):
        return self.image.name

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
