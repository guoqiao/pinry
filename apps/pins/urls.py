from django.conf.urls import patterns, url
from .views import PinCreateView, PinDeleteView

urlpatterns = patterns('pins.views',
    url(r'^$', 'recent_albums', name='recent-albums'),#show recent albums and paged by year
    url(r'^new-album/$', 'new_album', name='new-album'),# create new album
    url(r'^(?P<pk>\d+)/$', 'recent_pins', name='recent-pins'),
    url(r'^(?P<pk>\d+)/new-pin/$', 'new_pin', name='new-pin'),# add a new pin to current album
    (r'^(?P<pk>\d+)/upload/$', PinCreateView.as_view(), {}, 'upload'),
    (r'^/pin-delete/(?P<pk>\d+)$', PinDeleteView.as_view(), {}, 'pin-delete'),
    #url(r'^/album-delete/(\d+)$', PinDeleteView.as_view(), name='album-delete'),
)
