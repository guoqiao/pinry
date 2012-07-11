from django.conf.urls import patterns, url
#from .views import PinCreateView, PinDeleteView

urlpatterns = patterns('pins.views',
    url(r'^$', 'albums', name='albums'),
    url(r'^new-album/$', 'new_album', name='new-album'),

    url(r'^(?P<pk>\d+)/$', 'pins', name='pins'),
    url(r'^(?P<pk>\d+)/delete/$', 'delete_album', name='delete-album'),
    url(r'^(?P<pk>\d+)/download/$', 'download_album', name='download-album'),
    url(r'^(?P<pk>\d+)/upload/$', 'upload_pin', name='upload-pin'),

    url(r'^delete-pin/(?P<pk>\d+)/$', 'delete_pin', name='delete-pin'),
)
