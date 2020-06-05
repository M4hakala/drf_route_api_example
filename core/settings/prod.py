from .base import *
import json
from celery.schedules import crontab
import os


DEBUG = False

ALLOWED_HOSTS = os.getenv('APP_ALLOWED_HOSTS', 'nginx').split(',')

SECRET_KEY = os.getenv('APP_SECRET_KEY')

STATIC_ROOT = os.path.join(BASE_DIR, 'static')
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': os.getenv('POSTGRES_DB'),
        'USER': os.getenv('POSTGRES_USER'),
        'PASSWORD': os.getenv('POSTGRES_PASSWORD'),
        'HOST': 'db',
        'PORT': os.getenv('POSTGRES_PORT'),
        'TIMEZONE': 'UTC',
        'CLIENT_ENCODING': 'UTF8',
        'OPTIONS': json.loads(
            os.getenv('DATABASE_OPTIONS', '{}')
        ),
    }
}

CACHES = {
    'default': {
        'BACKEND': 'django_redis.cache.RedisCache',
        'LOCATION': f"redis://redis:{os.getenv('REDIS_PORT')}/0",
        'OPTIONS': {
            'CLIENT_CLASS': 'django_redis.client.DefaultClient',
        },
        "KEY_PREFIX": "api_route"
    },
}

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'verbose': {
            'format': '{asctime} {levelname} {module} {filename} {message}',
            'style': '{',
        },
        'console': {
            '()': 'django.utils.log.ServerFormatter',
            'format': '[{asctime}] [{process:d}] [{levelname}] {message}',
            'style': '{',
            'datefmt': '%Y-%m-%d %H:%M:%S',
        },
    },
    'handlers': {
        'mail_admins': {
            'class': 'django.utils.log.AdminEmailHandler',
            'level': 'ERROR',
            'include_html': True,
            'formatter': 'verbose',
        },
        'logfile': {
            'class': 'logging.handlers.WatchedFileHandler',
            'filename': './logs/app.log',
            'formatter': 'verbose',
            'level': 'INFO',
        },
        'console': {
            'level': 'WARNING',
            'class': 'logging.StreamHandler',
            'formatter': 'console',
        }
    },
    'loggers': {
        'django.request': {
            'handlers': ['mail_admins'],
            'level': 'ERROR',
            'propagate': False,
            'formatter': 'django.server',
        },
        'django.core.management': {
            'handlers': ['mail_admins'],
            'level': 'ERROR',
            'propagate': True,
            'formatter': 'django.server',
        },
        '': {
            'handlers': ['logfile', 'console'],
            'level': 'INFO',
        },
        'django': {
            'handlers': ['logfile', 'console'],
            'propagate': False,
            'level': 'INFO',
        },
        'api': {
            'handlers': ['logfile', 'console'],
            'propagate': False,
            'level': 'INFO',
        },
    },
}

CELERY_BROKER_URL = f"redis://redis:{os.getenv('REDIS_PORT')}/1"
CELERY_RESULT_BACKEND = f"redis://redis:{os.getenv('REDIS_PORT')}/1"
CELERY_ACCEPT_CONTENT = ['application/json']
CELERY_TASK_SERIALIZER = 'json'
CELERY_RESULT_SERIALIZER = 'json'

CELERY_BEAT_SCHEDULE = {
    'compute_longest_route': {
        'task': 'api.tasks.compute_longest_route',
        'schedule': crontab(minute=1, hour=12)
    },
}
