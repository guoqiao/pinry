from django.conf.urls import patterns, url
#from .views import PinCreateView, PinDeleteView

urlpatterns = patterns('pins.views',
    url(r'^$', 'recent_albums', name='recent-albums'),#show recent albums and paged by year
    url(r'^new-album/$', 'new_album', name='new-album'),# create new album

    url(r'^(?P<pk>\d+)/$', 'recent_pins', name='recent-pins'),
    url(r'^(?P<pk>\d+)/delete/$', 'delete_album', name='delete-album'),# create new album
    url(r'^(?P<pk>\d+)/new-pin/$', 'new_pin', name='new-pin'),# add a new pin to current album
    url(r'^(?P<pk>\d+)/upload/$', 'create_pin', name='upload'),
    url(r'^delete-pin/(?P<pk>\d+)/$', 'delete_pin', name='delete-pin'),
)
