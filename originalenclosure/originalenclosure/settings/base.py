import os
from os.path import join, abspath, dirname
from .secrets import *
import djcelery
djcelery.setup_loader()

nest = join(*3*['..'])
ROOT = abspath(join(dirname(__file__), nest))
TOP_FOLDER = join(ROOT, 'originalenclosure')

MEDIA_ROOT = join(ROOT, 'media')
STATIC_ROOT = join(ROOT, 'static')
MEDIA_URL = '/media/'
STATIC_URL = '/static/'


DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': POSTGRES_DB,
        'USER': POSTGRES_USER,
        'PASSWORD': POSTGRES_PASS,
        'HOST': '',
        'PORT': '',                      # Set to empty string for default. Not used with sqlite3.
    }
}

APPEND_SLASH = True

DEBUG = False
TEMPLATE_DEBUG = DEBUG

ADMINS = (
    # ('Your Name', 'your_email@example.com'),
)

MANAGERS = ADMINS

TIME_ZONE = 'Europe/London'

LANGUAGE_CODE = 'en-gb'

SITE_ID = 1

USE_I18N = True

USE_L10N = True

USE_TZ = True

STATICFILES_DIRS = (
)

STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
#    'django.contrib.staticfiles.finders.DefaultStorageFinder',
)

TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.Loader',
    'django.template.loaders.app_directories.Loader',
)

MIDDLEWARE_CLASSES = (
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
)

ROOT_URLCONF = 'originalenclosure.urls'

WSGI_APPLICATION = 'originalenclosure.wsgi.application'

TEMPLATE_DIRS = (
    join(TOP_FOLDER, 'templates'),
)

INSTALLED_APPS = (
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.admin',
    'djcelery',
    'south',
    'django_nose',
    'originalenclosure',
    'pars',
    'werkzeug_debugger_runserver',
)

TEST_RUNNER = 'django_nose.NoseTestSuiteRunner'
NOSE_ARGS = ['--nologcapture']

GUMROAD_API_URL = 'https://api.gumroad.com/v1/links'
DOMAIN = 'http://www.originalenclosure.net'
