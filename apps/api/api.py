from django.contrib.auth.models import User
from tastypie import fields
#from tastypie.authorization import Authorization
from tastypie.resources import ModelResource, ALL_WITH_RELATIONS
#from tastypie.resources import ModelResource, ALL, ALL_WITH_RELATIONS

from pins.models import Pin,Album

class UserResource(ModelResource):
    class Meta:
        queryset = User.objects.all()
        resource_name = 'user'
        excludes = ['email', 'password', 'is_active', 'is_staff', 'is_superuser']
        filtering = {
            'username': ALL_WITH_RELATIONS,
        }

class AlbumResource(ModelResource):
    user = fields.ForeignKey(UserResource, 'user')
    class Meta:
        queryset = Album.objects.all()
        resource_name = 'album'
        include_resource_uri = False
        filtering = {
            'user': ALL_WITH_RELATIONS,
            'create': ['exact', 'lt', 'lte', 'gte', 'gt'],
        }

class PinResource(ModelResource):  # pylint: disable-msg=R0904
    album = fields.ForeignKey(AlbumResource, 'album')
    thumbnail = fields.CharField(readonly=True)

    class Meta:
        queryset = Pin.objects.all()
        resource_name = 'pin'
        include_resource_uri = False
        filtering = {
            'album': ALL_WITH_RELATIONS,
        }

    def dehydrate_thumbnail(self, bundle):
        pin = Pin.objects.only('file').get(pk=bundle.data['id'])
        return pin.file.url_200x1000

