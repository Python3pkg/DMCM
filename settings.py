import sys
# Django settings for userid project.

SITE_ROOT_ID = 3 # Homepage
BLOG_ROOT_ID = 1

DEBUG = True
TEMPLATE_DEBUG = DEBUG

ADMINS = (
    # ('Paul Ahern', 'userid@userid.com'),
)

MANAGERS = ADMINS

DATABASE_ENGINE = 'mysql'            # 'postgresql_psycopg2', 'postgresql', 'mysql', 'sqlite3' or 'oracle'.
DATABASE_NAME = 'dmcm'      # Or path to database file if using sqlite3.
DATABASE_USER = 'root'             # Not used with sqlite3.
DATABASE_PASSWORD = ''         # Not used with sqlite3.
DATABASE_HOST = ''             # Set to empty string for localhost. Not used with sqlite3.
DATABASE_PORT = ''             # Set to empty string for default. Not used with sqlite3.

# Local time zone for this installation. Choices can be found here:
# http://en.wikipedia.org/wiki/List_of_tz_zones_by_name
# although not all choices may be available on all operating systems.
# If running in a Windows environment this must be set to the same as your
# system time zone.
TIME_ZONE = 'Europe/London'

# Language code for this installation. All choices can be found here:
# http://www.i18nguy.com/unicode/language-identifiers.html
LANGUAGE_CODE = 'en-gb'

SITE_ID = 1

# If you set this to False, Django will make some optimizations so as not
# to load the internationalization machinery.
USE_I18N = True

# Absolute path to the directory that holds media.
# Example: "/home/media/media.lawrence.com/"
MEDIA_ROOT = '/home/ahernp/Documents/ahernp.com/site/'

# URL that handles the media served from MEDIA_ROOT. Make sure to use a
# trailing slash if there is a path component (optional in other cases).
# Examples: "http://media.lawrence.com", "http://example.com/media/"
MEDIA_URL = '/static/'

# URL prefix for admin media -- CSS, JavaScript and images. Make sure to use a
# trailing slash.
# Examples: "http://foo.com/media/", "/media/".
ADMIN_MEDIA_PREFIX = '/site_media/admin/'

# Make this unique, and don't share it with anybody.
SECRET_KEY = ''

from django.conf.global_settings import TEMPLATE_CONTEXT_PROCESSORS
TEMPLATE_CONTEXT_PROCESSORS += (
    "dmcm.cm.utils.context_processor",
)

# List of callables that know how to import templates from various sources.
TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.load_template_source',
    'django.template.loaders.app_directories.load_template_source',
    'django.template.loaders.eggs.load_template_source',
)

MIDDLEWARE_CLASSES = (
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.middleware.transaction.TransactionMiddleware',
    'reversion.middleware.RevisionMiddleware',
)

ROOT_URLCONF = 'dmcm.urls'

TEMPLATE_DIRS = (
    '/home/ahernp/code/dmcm/dmcm/templates'
)

INSTALLED_APPS = (
    'django.contrib.auth',
    'django.contrib.admin',
    'django.contrib.admindocs',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.markup',
    'reversion',
    'dmcm.cm',
)

#import logging
#logging.basicConfig(
#    level = logging.DEBUG,
#    format = '%(asctime)s %(levelname)s %(message)s',
#    filename = '/home/ahernp/code/dmcm/dmcm.log',
#    filemode = 'w'
#)
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