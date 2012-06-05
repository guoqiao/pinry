from django.conf.urls import patterns, url

urlpatterns = patterns('pins.views',
    #url(r'^$', 'recent_pins', name='recent-pins'),
    url(r'^$', 'recent_albums', name='recent-albums'),
    url(r'^new-pin/$', 'new_pin', name='new-pin'),
    url(r'^new-album/$', 'new_album', name='new-album'),
)
