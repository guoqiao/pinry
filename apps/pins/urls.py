from django.conf.urls import patterns, url

urlpatterns = patterns('pins.views',
    url(r'^$', 'recent_albums', name='recent-albums'),#show recent albums and paged by year
    url(r'^new-album/$', 'new_album', name='new-album'),# create new album
    url(r'^(\d+)/$', 'recent_pins', name='recent-pins'),
    url(r'^(\d+)/new-pin/$', 'new_pin', name='new-pin'),# add a new pin to current album
)
