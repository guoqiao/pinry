from django.conf.urls import patterns, url
#from .views import PinCreateView, PinDeleteView

urlpatterns = patterns('pins.pin_views',
    url(r'^$', 'home', name='home'),
    url(r'^delete/$', 'delete', name='delete'),
    url(r'^rotate/$', 'rotate', name='rotate'),
    url(r'^nav/$', 'nav', name='nav'),
)
