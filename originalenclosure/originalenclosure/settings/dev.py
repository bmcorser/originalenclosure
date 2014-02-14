from .base import *

DOMAIN = 'http://localhost:8000'

DEBUG = True
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(ROOT, 'originalenclosure', 'development.db'),
        'USER': '',
        'PASSWORD': '',
        'HOST': '',
        'PORT': '',
    }
}
CELERY_RESULT_BACKEND = "redis://localhost/9"
BROKER_URL = "amqp://guest:guest@localhost:5672//"
INSTALLED_APPS += ('werkzeug_debugger_runserver',)
