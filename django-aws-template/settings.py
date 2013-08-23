# Django settings for cardea project.
import os
import sys
from cardea.metaconfig import Metaconfig

DEPLOY_ROOT='/var/cardea'
SECRETS_FILE='.secrets'

CONTRIB_LIBS_DIR=os.path.join(os.getcwd(), 'src', 'contrib', 'libs')

sys.path.append(CONTRIB_LIBS_DIR)

Metaconfig.load(DEPLOY_ROOT, SECRETS_FILE)

BROKER_URL = Metaconfig.get('CLOUDAMQP_URL')
ENV = Metaconfig.get('CARDEA_ENV')
#DEBUG = True
#TEMPLATE_DEBUG = DEBUG
FE_TESTING = Metaconfig.get('FE_TESTING')

ADMINS = (
    # ('Your Name', 'your_email@example.com'),
)

#os.environ['DJANGO_SETTINGS_MODULE'] = 'cardeahome.settings'

MANAGERS = ADMINS

#DATABASES = {
#    'default': {
#        'ENGINE': 'django.db.backends.mysql', # Add 'postgresql_psycopg2', 'postgresql', 'mysql', 'sqlite3' or 'oracle'.
#        'NAME': 'cardea',                      # Or path to database file if using sqlite3.
#        'USER': 'cardearw',                      # Not used with sqlite3.
#        'PASSWORD': 'cardearwpass',                  # Not used with sqlite3.
#        'HOST': '',                      # Set to empty string for localhost. Not used with sqlite3.
#        'PORT': '',                      # Set to empty string for default. Not used with sqlite3.
#    }
#}

# Local time zone for this installation. Choices can be found here:
# http://en.wikipedia.org/wiki/List_of_tz_zones_by_name
# although not all choices may be available on all operating systems.
# On Unix systems, a value of None will cause Django to use the same
# timezone as the operating system.
# If running in a Windows environment this must be set to the same as your
# system time zone.
TIME_ZONE = 'America/Los_Angeles'

# Language code for this installation. All choices can be found here:
# http://www.i18nguy.com/unicode/language-identifiers.html
LANGUAGE_CODE = 'en-us'

SITE_ID = 1

USE_TZ = False

# If you set this to False, Django will make some optimizations so as not
# to load the internationalization machinery.
USE_I18N = True

# If you set this to False, Django will not format dates, numbers and
# calendars according to the current locale
USE_L10N = True

# Absolute filesystem path to the directory that will hold user-uploaded files.
# Example: "/home/media/media.lawrence.com/media/"
MEDIA_ROOT = ''

# URL that handles the media served from MEDIA_ROOT. Make sure to use a
# trailing slash.
# Examples: "http://media.lawrence.com/media/", "http://example.com/media/"
MEDIA_URL = ''

# Absolute path to the directory static files should be collected to.
# Don't put anything in this directory yourself; store your static files
# in apps' "static/" subdirectories and in STATICFILES_DIRS.
# Example: "/home/media/media.lawrence.com/static/"
STATIC_ROOT = 'src/cardeahome/staticfiles'

# URL prefix for static files.
# Example: "http://media.lawrence.com/static/"
STATIC_URL = '/static/'

# URL prefix for admin static files -- CSS, JavaScript and images.
# Make sure to use a trailing slash.
# Examples: "http://foo.com/static/admin/", "/static/admin/".
ADMIN_MEDIA_PREFIX = '/static/admin/'

# Additional locations of static files
STATICFILES_DIRS = (
    # Put strings here, like "/home/html/static" or "C:/www/django/static".
    # Always use forward slashes, even on Windows.
    # Don't forget to use absolute paths, not relative paths.
    'src/cardeahome/static',
)

# List of finder classes that know how to find static files in
# various locations.
STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
#    'django.contrib.staticfiles.finders.DefaultStorageFinder',
)

# Make this unique, and don't share it with anybody.
SECRET_KEY = 'hw%z_vo&l&s9mg&a55=ng6ojp^-4b)6a@l!7dpp!8oz#5bva&n'

# List of callables that know how to import templates from various sources.
TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.Loader',
    'django.template.loaders.app_directories.Loader',
#     'django.template.loaders.eggs.Loader',
)

MIDDLEWARE_CLASSES = (
#    'hirefire.contrib.django.middleware.HireFireMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django_hosts.middleware.HostsMiddleware',
)

#HIREFIRE_PROCS = ['cardea.service.task.procs.WorkerProc']
#HIREFIRE_TOKEN = os.environ.get('HIREFIRE_TOKEN')

ROOT_URLCONF = 'urls'

ROOT_HOSTCONF = 'hosts'

DEFAULT_HOST = 'www'
 
FIXTURE_DIRS = (
    'src/cardeahome/cardea/account'
)

TEMPLATE_DIRS = (
    # Put strings here, like "/home/html/django_templates" or "C:/www/django/templates".
    # Always use forward slashes, even on Windows.
    # Don't forget to use absolute paths, not relative paths.
    'src/cardeahome/templates'
)

BASE_INSTALLED_APPS = [
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    # Uncomment the next line to enable the admin:
    'django.contrib.admin',
    # Uncomment the next line to enable admin documentation:
    # 'django.contrib.admindocs',
    'django_hosts',
    'cardea.api',
    'cardea.pub',
    'cardea.cadmin',
    'cardea.account',
    'cardea.keydb',
    'cardea.product',
    'cardea.recalls',
    'cardea.safety',
    'cardea.service',
    'cardea.sources',
    'cardea.standalone'
]

CACHE_MIDDLEWARE_ANONYMOUS_ONLY=True

import djcelery
djcelery.setup_loader()
DEBUG = False
CELERY_IMPORTS = (
    'cardea.service.task.definitions'
)

BROKER_POOL_LIMIT = 1
CELERYD_CONCURRENCY = 1

BASE_INSTALLED_APPS.append('djcelery')

INSTALLED_APPS = tuple(BASE_INSTALLED_APPS)

# A sample logging configuration. The only tangible logging
# performed by this configuration is to send an email to
# the site admins on every HTTP 500 error.
# See http://docs.djangoproject.com/en/dev/topics/logging for
# more details on how to customize your logging configuration.
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'super_verbose': {
            'format': '%(levelname)s %(asctime)s %(module)s %(process)d %(thread)d %(message)s'
        },
        'verbose': {
            'format': '%(levelname)s %(asctime)s %(module)s %(message)s'
        },
        'simple': {
            'format': '%(levelname)s $(asctime)s %(message)s'
        },
    },
    'handlers': {
        'mail_admins': {
            'level': 'ERROR',
            'class': 'django.utils.log.AdminEmailHandler'
        },
        'console':{
            'level':'DEBUG',
            'class':'logging.StreamHandler',
            'stream': sys.stdout
        },
        'log_file':{
            'level':'DEBUG',
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': '/var/log/cardea.log',
            'maxBytes': '16777216', # 16megabytes
            'formatter': 'verbose'            
        },
        'parse_log_file':{
            'level':'INFO',
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': '/var/log/cardea-parse.log',
            'maxBytes': '16777216', # 16megabytes
            'formatter': 'verbose'
        },
        'notifications_log_file':{
            'level': 'INFO',
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': '/var/log/cardea-notifications.log',
            'maxBytes': '16777216', # 16megabytes
            'formatter': 'verbose'
        }
    },
    'loggers': {
        '': {
            'handlers': ['console','log_file'],
            'level': 'DEBUG',
            'propagate': True,
            'filters': []
        },
        'parse': {
            'handlers': ['console', 'parse_log_file'],
            'level': 'DEBUG',
            'propagate': True,
            'filters': []
        },
        'notifications': {
            'handlers': ['console', 'notifications_log_file'],
            'level': 'INFO',
            'propagate': True,
            'filters': []
        },
        'django.request': {
            'handlers': ['log_file'],
            'level': 'DEBUG',
            'propagate': True,
            'filters': []
        },
    }
}


import os
import sys
import urlparse

# 'dev' is strictly for running Django runserver
if ENV == 'dev' or ENV == 'stage':
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.mysql',
            'NAME': 'cardea',
            'USER': 'cardearw',
            'PASSWORD': 'cardearwpass',
            'HOST': 'localhost'
        }
    }
# 'stage' is for running via foreman
# 'prod' is running in Heroku
elif ENV == 'prod':
    # Parse database configuration from $DATABASE_URL
    import dj_database_url
    DATABASES = {'default': dj_database_url.config(default=Metaconfig.get('DATABASE_URL'))}