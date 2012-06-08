from django.conf.urls import patterns, include, url
from django.conf.urls.static import static
from django.conf import settings

from tastypie.api import Api
from api.api import AlbumResource,PinResource

v1_api = Api(api_name='v1')
v1_api.register(AlbumResource())
v1_api.register(PinResource())

urlpatterns = patterns('',
    url(r'', include(v1_api.urls)),
)

urlpatterns = patterns('',
    url(r'', include('core.urls', namespace='core')),
    url(r'^pins/', include('pins.urls', namespace='pins')),
    url(r'^api/', include(v1_api.urls)),
) + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
