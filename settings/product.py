from base import * 
DEBUG = True
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'

#devserver
MIDDLEWARE_CLASSES += ()   # Add extra classes here
INSTALLED_APPS += ()       # Add extra apps here

MEDIA_URL  = 'http://10.10.20.173/pinry_media/'
STATIC_URL = 'http://10.10.20.173/pinry_static/'
STATIC_ROOT = os.path.join(PROJECT_ROOT, 'static')
