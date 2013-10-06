from .base import *
from celery.schedules import crontab
import os

TOP_FOLDER = os.path.abspath(os.path.join(os.path.dirname(__file__), '../..'))

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

MEDIA_ROOT = ''

MEDIA_URL = ''

STATIC_ROOT = ''

STATIC_URL = '/static/'

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
    os.path.join(TOP_FOLDER, 'templates'),
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

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'filters': {
        'require_debug_false': {
            '()': 'django.utils.log.RequireDebugFalse'
        }
    },
    'handlers': {
        'mail_admins': {
            'level': 'ERROR',
            'filters': ['require_debug_false'],
            'class': 'django.utils.log.AdminEmailHandler'
        }
    },
    'loggers': {
        'django.request': {
            'handlers': ['mail_admins'],
            'level': 'ERROR',
            'propagate': True,
        },
    }
}

import djcelery
djcelery.setup_loader()
CELERY_RESULT_BACKEND = "redis://localhost/7"
BROKER_URL = "amqp://guest:guest@localhost:5672//"

CELERYBEAT_SCHEDULE = {
    'pars-buffer': {
        'task': 'pars.tasks.facebook',
        'schedule': crontab(day_of_week='tue,thu',hour=18)
    },
    'celery-test': {
        'task': 'originalenclosure.tasks.celery_test',
        'schedule': crontab()
    }
}

APPEND_SLASH = True

GUMROAD_API_URL = 'https://api.gumroad.com/v1/links'

try:
    from local_settings import *
except ImportError:
    raise ImportError('mv local_settings.py.template local_settings.py && vi local_settings.py')
