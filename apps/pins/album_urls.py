from django.conf.urls import patterns, url
#from .views import PinCreateView, PinDeleteView

urlpatterns = patterns('pins.album_views',
    url(r'^$', 'list', name='list'),
    url(r'^new/$', 'new', name='new'),
    url(r'^comments/$', 'comments', name='comments'),
    url(r'^(?P<pk>\d+)/$', 'home', name='home'),
    url(r'^(?P<pk>\d+)/upload/$', 'upload', name='upload'),
    url(r'^(?P<pk>\d+)/delete/$', 'delete', name='delete'),
    url(r'^(?P<pk>\d+)/download/$', 'download', name='download'),
)
