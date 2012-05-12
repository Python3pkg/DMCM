"""Django settings for dmcm project."""
import sys

SITE_ROOT_ID = 3 # Homepage
BLOG_ROOT_ID = 1

DEBUG = False
DEVELOP = False
TEMPLATE_DEBUG = DEBUG

ADMINS = (
     ('Paul Ahern', 'ahernp@ahernp.com'),
)

MANAGERS = ADMINS

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'dmcm'
    }
}

TIME_ZONE = 'Europe/London'
LANGUAGE_CODE = 'en-gb'
SITE_ID = 1
USE_I18N = True
MEDIA_ROOT = '/home/ahernp/Documents/ahernp.com/site/'
MEDIA_URL = '/media/'
ADMIN_MEDIA_PREFIX = '/static/admin/'
STATIC_ROOT = '/home/ahernp/code/dmcm/static/'
STATIC_URL = '/static/'
#SECRET_KEY = '' # Populated in localsettings.py
TEMPLATE_CONTEXT_PROCESSORS = (
    'django.core.context_processors.debug',
    'django.core.context_processors.i18n',
    'django.core.context_processors.media',
    'django.core.context_processors.static',
    'django.contrib.auth.context_processors.auth',
    'django.contrib.messages.context_processors.messages',
    'project.dmcm.context_processors.context_processor',
)
MIDDLEWARE_CLASSES = (
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.middleware.transaction.TransactionMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'reversion.middleware.RevisionMiddleware',
)
ROOT_URLCONF = 'project.urls'
TEMPLATE_DIRS = (
    '/home/ahernp/code/dmcm/project/templates'
)
INSTALLED_APPS = (
    'django.contrib.auth',
    'django.contrib.admin',
    'django.contrib.admindocs',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.staticfiles',
    'django.contrib.markup',
    'reversion',
    'project.dmcm',
)

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
