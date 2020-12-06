# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, unicode_literals, print_function

from . import *
from datetime import timedelta

# Flask-mongoengine :
MONGODB_SETTINGS = {
    'host': os.environ.get('DATABASE_URL'),
    'password': os.environ.get('MONGODB_PASSWORD'),
    'username': os.environ.get('MONGODB_USERNAME'),
    'tz_aware': True,
}

# Redis Cache :
REDIS_URL = os.environ.get('REDIS_URL','redis://localhost:6379/3')

# Celery :
CELERY_BROKER_URL = os.environ.get('CELERY_BROKER_URL','redis://localhost:6379/1')
CELERY_RESULT_BACKEND = os.environ.get('CELERY_RESULT_BACKEND','redis://localhost:6379/2')
CELERY_ENABLE_UTC = True
CELERY_TIMEZONE = os.environ.get('CELERY_TIMEZONE') or 'Asia/Taipei'
CELERYD_LOG_FORMAT = '%(asctime)s stdout F [%(levelname)s]%(message)s}'
CELERY_TASK_SERIALIZER = os.environ.get('CELERY_TASK_SERIALIZER') or 'json'
CELERY_RESULT_SERIALIZER = os.environ.get('CELERY_RESULT_SERIALIZER') or 'json'
CELERY_MESSAGE_COMPRESSION = os.environ.get('CELERY_MESSAGE_COMPRESSION') or 'json'
CELERY_TASK_RESULT_EXPIRES = os.environ.get('CELERY_TASK_RESULT_EXPIRES') or 600
CELERY_ACCEPT_CONTENT = (os.environ.get('CELERY_ACCEPT_CONTENT') or ' '.join(['json'])).split()

CELERY_ALWAYS_EAGER = (os.environ.get('CELERY_ALWAYS_EAGER') or 'false').lower() in ('t', 'true', '1')

LOG_FILE_PATH = os.environ.get('LOG_FILE_PATH') or 'hotel.log'
ERROR_LOG_FILE_PATH = os.environ.get('ERROR_LOG_FILE_PATH') or 'hotel.log'


CELERYBEAT_SCHEDULE = {
    'crawler': {
        'task': 'hotel.tasks.crawler',
        'schedule': timedelta(days=1)
    },
}