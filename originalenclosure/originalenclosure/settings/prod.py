from .base import *
from celery.schedules import crontab


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
