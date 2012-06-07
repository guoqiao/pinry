# -*- coding: UTF-8 -*-
# Django settings for SPIG Django projects.
import os, sys
HERE = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.join(HERE, '../')
APPS_ROOT = os.path.join(PROJECT_ROOT, 'apps')

#SITE_URL = "http://iot-oa.insigma.com.cn"

sys.path.insert(0, PROJECT_ROOT)
sys.path.insert(0, APPS_ROOT)

DEBUG = True
TEMPLATE_DEBUG = DEBUG

ADMINS = (
    ('Guo Qiao', 'guoqiao@insigma.com.cn'),
)

MANAGERS = ADMINS

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',            # Add 'postgresql_psycopg2', 'postgresql', 'mysql', 'sqlite3' or 'oracle'.
        'NAME': os.path.join(PROJECT_ROOT, 'dev.db'),   # Or path to database file if using sqlite3.
        'USER': '',                      # Not used with sqlite3.
        'PASSWORD': '',                  # Not used with sqlite3.
        'HOST': '',                      # Set to empty string for localhost. Not used with sqlite3.
        'PORT': '',                      # Set to empty string for default. Not used with sqlite3.
    }
}

# Local time zone for this installation. Choices can be found here:
# http://en.wikipedia.org/wiki/List_of_tz_zones_by_name
# although not all choices may be available on all operating systems.
# On Unix systems, a value of None will cause Django to use the same
# timezone as the operating system.
# If running in a Windows environment this must be set to the same as your
# system time zone.
TIME_ZONE = 'Asia/Hong_Kong'

# Language code for this installation. All choices can be found here:
# http://www.i18nguy.com/unicode/language-identifiers.html
LANGUAGE_CODE = 'zh-cn'

SITE_ID = 1

# If you set this to False, Django will make some optimizations so as not
# to load the internationalization machinery.
USE_I18N = True

# If you set this to False, Django will not format dates, numbers and
# calendars according to the current locale
USE_L10N = True

# Absolute filesystem path to the directory that will hold user-uploaded files.
# Example: "/home/media/media.lawrence.com/media/"
MEDIA_ROOT = os.path.join(PROJECT_ROOT, 'media')

# URL that handles the media served from MEDIA_ROOT. Make sure to use a
# trailing slash.
# Examples: "http://media.lawrence.com/media/", "http://example.com/media/"
MEDIA_URL = '/media/'

# Absolute path to the directory static files should be collected to.
# Don't put anything in this directory yourself; store your static files
# in apps' "static/" subdirectories and in STATICFILES_DIRS.
# Example: "/home/media/media.lawrence.com/static/"
STATIC_ROOT = os.path.join(PROJECT_ROOT, 'collectedstatic')

# URL prefix for static files.
# Example: "http://media.lawrence.com/static/"
STATIC_URL = '/static/'

# URL prefix for admin static files -- CSS, JavaScript and images.
# Make sure to use a trailing slash.
# Examples: "http://foo.com/static/admin/", "/static/admin/".
ADMIN_MEDIA_PREFIX = '/static/admin/'

# Additional locations of static files
STATICFILES_DIRS = (
    os.path.join(PROJECT_ROOT, 'static/'),
    # Put strings here, like "/home/html/static" or "C:/www/django/static".
    # Always use forward slashes, even on Windows.
    # Don't forget to use absolute paths, not relative paths.
)

# List of finder classes that know how to find static files in
# various locations.
STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
)

# Make this unique, and don't share it with anybody.
SECRET_KEY = '' # '&(^z)7qj1!2by^q%v3&bmwgasm+1ts_kfr0eu(h%4fipyukt'

# List of callables that know how to import templates from various sources.
TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.Loader',
    'django.template.loaders.app_directories.Loader',
)

MIDDLEWARE_CLASSES = (
    'django.middleware.locale.LocaleMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    #'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
)

ROOT_URLCONF = 'urls'

TEMPLATE_DIRS = (
    # Put strings here, like "/home/html/django_templates" or "C:/www/django/templates".
    # Always use forward slashes, even on Windows.
    # Don't forget to use absolute paths, not relative paths.
    os.path.join(PROJECT_ROOT, 'templates'),
)

TEMPLATE_CONTEXT_PROCESSORS = (
        "django.contrib.auth.context_processors.auth",
        "django.core.context_processors.debug",
        "django.core.context_processors.i18n",
        "django.core.context_processors.media",
        "django.core.context_processors.static",
        "django.core.context_processors.request",
        "django.contrib.messages.context_processors.messages",
)

WSGI_APPLICATION = 'wsgi.application'
LOGIN_REDIRECT_URL = '/'
INTERNAL_IPS = ['127.0.0.1']

from django.contrib.messages import constants as messages
MESSAGE_TAGS = {
    messages.WARNING: 'alert',
    messages.ERROR: 'alert alert-error',
    messages.SUCCESS: 'alert alert-success',
    messages.INFO: 'alert alert-info',
}
API_LIMIT_PER_PAGE = 20

INSTALLED_APPS = (
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    # Uncomment the next line to enable the admin:
    'django.contrib.admin',
    # Uncomment the next line to enable admin documentation:
    'django_wsgiserver',
    'core',
    'pins',
    'api',
)


LOGIN_REDIRECT_URL = '/'
LOGOUT_URL = "/"

AUTHENTICATION_BACKENDS = (
    'django_auth_ldap.backend.LDAPBackend',
    'django.contrib.auth.backends.ModelBackend',
)

# == LDAP ==
AUTH_LDAP_SERVER_URI = "ldap://10.10.20.220:389"

import ldap
from django_auth_ldap.config import GroupOfUniqueNamesType
from django_auth_ldap.config import LDAPSearch

AUTH_LDAP_BIND_DN = "cn=Directory Manager"
AUTH_LDAP_BIND_PASSWORD = "ab12cd"
AUTH_LDAP_USER_SEARCH = LDAPSearch("ou=users,ou=staff,dc=insigma,dc=com", \
        ldap.SCOPE_SUBTREE, "(cn=%(user)s)")
AUTH_LDAP_USER_BASE_SEARCH = LDAPSearch("ou=users,ou=staff,dc=insigma,dc=com", \
        ldap.SCOPE_SUBTREE, "(objectClass=organizationalPerson)")
AUTH_LDAP_GROUP_SEARCH = LDAPSearch("ou=groups,ou=staff,dc=insigma,dc=com", \
    ldap.SCOPE_SUBTREE, "(objectClass=groupOfUniqueNames)"
)
AUTH_LDAP_GROUP_TYPE = GroupOfUniqueNamesType()
AUTH_LDAP_MIRROR_GROUPS = True

LDAP_USER_BASE_DN = "ou=users,ou=staff,dc=insigma,dc=com"
LDAP_GROUP_BASE_DN = "ou=groups,ou=staff,dc=insigma,dc=com"
LDAP_USER_DEFAULT_GROUPS = ('IOT.ALL', 'confluence-users', 'jira-users', 'jira-developers')
LDAP_INACTIVE_BASE_DN = 'ou=inactive,ou=staff,dc=insigma,dc=com'

# == EMAIL ==
EMAIL_HOST='smtp.insigma.com.cn'
EMAIL_PORT='587'
EMAIL_HOST_USER='spig@insigma.com.cn'
EMAIL_HOST_PASSWORD='123456'
DEFAULT_FROM_EMAIL='spig@insigma.com.cn'

# celery
#import djcelery
#djcelery.setup_loader()
#BROKER_URL = "django://"
ALBUM_ROOT = os.path.join(MEDIA_ROOT,'albums')
