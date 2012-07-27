from django.conf.urls import patterns, url


urlpatterns = patterns('',
    url(r'^$', 'core.views.home', name='home'),
    url(r'^login/$', 'django.contrib.auth.views.login',{'template_name': 'core/login.html'}, name='login'),
    url(r'^register/$', 'core.views.register', name='register'),
    url(r'^logout/$', 'core.views.logout_user', name='logout'),
)
