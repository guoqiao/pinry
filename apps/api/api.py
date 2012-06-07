from tastypie.resources import ModelResource
from tastypie import fields

from pins.models import Pin,Album


class PinResource(ModelResource):  # pylint: disable-msg=R0904
    thumbnail = fields.CharField(readonly=True)

    class Meta:
        queryset = Pin.objects.all()
        resource_name = 'pin'
        include_resource_uri = False

    def dehydrate_thumbnail(self, bundle):
        pin = Pin.objects.only('image').get(pk=bundle.data['id'])
        return pin.image.url_200x1000

class AlbumResource(ModelResource):
    class Meta:
        queryset = Album.objects.all()
        resource_name = 'album'
        include_resource_uri = False
