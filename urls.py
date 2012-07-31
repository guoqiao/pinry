from django.conf.urls import patterns, include, url
from django.conf.urls.static import static
from django.conf import settings
from django.contrib import admin
admin.autodiscover()

from tastypie.api import Api
from api.api import AlbumResource,PinResource,UserResource

v1_api = Api(api_name='v1')
v1_api.register(UserResource())
v1_api.register(AlbumResource())
v1_api.register(PinResource())

urlpatterns = patterns('',
    url(r'^albums/', include('pins.album_urls', namespace='album')),
    url(r'^pins/(?P<pk>\d+)/', include('pins.pin_urls', namespace='pin')),
    url(r'^api/', include(v1_api.urls)),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^comments/', include('django.contrib.comments.urls')),
    url(r'', include('core.urls', namespace='core')),
)

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
