from .base import *
import json
import os


DEBUG = os.getenv('DEBUG', True)

ALLOWED_HOSTS = os.getenv('APP_ALLOWED_HOSTS', '*').split(',')

SECRET_KEY = os.getenv('APP_SECRET_KEY', '2q8dw7aio-4bh4mv_zq2#6x$atf5mkwx$^abn0t4twvb8p8%-#')

STATIC_ROOT = os.path.join(BASE_DIR, 'static')
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': os.getenv('DB_PG_DB'),
        'USER': os.getenv('DB_PG_USER'),
        'PASSWORD': os.getenv('DB_PG_PASS'),
        'HOST': 'localhost',
        'PORT': os.getenv('DB_PG_PORT'),
        'TIMEZONE': 'UTC',
        'CLIENT_ENCODING': 'UTF8',
        'OPTIONS': json.loads(
            os.getenv('DATABASE_OPTIONS', '{}')
        ),
    }
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
        'logfile': {
            'class': 'logging.handlers.WatchedFileHandler',
            'filename': './logs/app.log',
            'formatter': 'verbose',
            'level': 'DEBUG',
        },
        'console': {
            'level': 'WARNING',
            'class': 'logging.StreamHandler',
            'formatter': 'console',
        }
    },
    'loggers': {
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
