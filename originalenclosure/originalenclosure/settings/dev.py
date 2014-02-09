from .base import *
DOMAIN = 'http://www.originalenclosure.net:8000'
nest = join(*2*['..'])
ROOT = abspath(join(dirname(__file__), nest))
TOP_FOLDER = join(ROOT, 'originalenclosure')

MEDIA_ROOT = join(ROOT, 'media')
STATIC_ROOT = join(ROOT, 'static')
MEDIA_URL = '/media/'
STATIC_URL = '/static/'

DEBUG = True
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(TOP_FOLDER, 'development.db'),
        'USER': '',
        'PASSWORD': '',
        'HOST': '',
        'PORT': '',
    }
}
CELERY_RESULT_BACKEND = "redis://localhost/9"
BROKER_URL = "amqp://guest:guest@localhost:5672//"
# INSTALLED_APPS += ('werkzeug_debugger_runserver',)
