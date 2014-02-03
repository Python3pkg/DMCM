"""Django settings for ahernp.com project."""
import sys
import os

PROJECT_PATH = os.path.dirname(os.path.realpath(__file__))

SITE_ROOT_SLUG = 'ahernp-com'  # Homepage
BLOG_ROOT_SLUG = 'blog'

DEBUG = False
DEVELOP = False
TEMPLATE_DEBUG = DEBUG

ADMINS = (('Your Name', 'your_email@example.com'),)
MANAGERS = ADMINS
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'dmcm',                      
        'USER': '',
        'PASSWORD': '',
        'HOST': ''
    }
}
TIME_ZONE = 'Europe/London'
USE_TZ = True
LANGUAGE_CODE = 'en-gb'
DATE_FORMAT = 'Y-m-d'  # yyyy-mm-dd
DATETIME_FORMAT = 'Y-m-d H:i'  # yyyy-mm-dd hh:mm
TIME_FORMAT = 'H:i'
SITE_ID = 1
USE_I18N = True
MEDIA_ROOT = os.path.join(PROJECT_PATH, os.pardir, 'media')
MEDIA_URL = '/media/'
ADMIN_MEDIA_PREFIX = '/static/admin/'
STATICFILES_DIRS = (os.path.join(PROJECT_PATH, 'static'),)
STATIC_ROOT = os.path.join(PROJECT_PATH, os.pardir, 'static')
STATIC_URL = '/static/'
TEMPLATE_CONTEXT_PROCESSORS = (
    'django.core.context_processors.debug',
    'django.core.context_processors.i18n',
    'django.core.context_processors.media',
    'django.core.context_processors.static',
    'django.core.context_processors.request',
    'django.contrib.auth.context_processors.auth',
    'django.contrib.messages.context_processors.messages',
    'dmcm.context_processors.context_processor',
)
MIDDLEWARE_CLASSES = (
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'reversion.middleware.RevisionMiddleware',
)
ROOT_URLCONF = 'urls'
TEMPLATE_DIRS = (
    os.path.join(PROJECT_PATH, 'templates')
)
INSTALLED_APPS = (
    'django.contrib.auth',
    'django.contrib.admin',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.staticfiles',
    'bugtracker',
    'dmcm',
    'blog',
    'feedreader',
    'monitoring',
    'reversion',
)

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'db_log': {
            'level': 'INFO',
           # Reference to handler in log.py below
            'class': 'monitoring.log.DbLogHandler',
        }
    },
    'loggers': {
        'feedreader': {
            'handlers': ['db_log', ],
            'level': 'INFO',
            'propagate': True,
        },
    }
}

try:
    from localsettings import *
except ImportError:
    print >> sys.stderr, """
    -------------------------------------------------------------------------
    Passwords and other confidential settings are held in a localsettings.py
    on the server but not in the code repository.
    -------------------------------------------------------------------------
    """
    sys.exit(1)
