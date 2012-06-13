from django.conf.urls import patterns, include, url
from django.conf.urls.static import static
from django.conf import settings

from tastypie.api import Api
from api.api import AlbumResource,PinResource,UserResource

v1_api = Api(api_name='v1')
v1_api.register(UserResource())
v1_api.register(AlbumResource())
v1_api.register(PinResource())

urlpatterns = patterns('',
    url(r'^albums/', include('pins.urls', namespace='pins')),
    url(r'^api/', include(v1_api.urls)),
    url(r'', include('core.urls', namespace='core')),
) + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
