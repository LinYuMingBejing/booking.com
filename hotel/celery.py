# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, unicode_literals, print_function

import os

import raven
import hotel

from celery import Celery as BaseCelery
from raven.contrib.celery import register_signal, register_logger_signal


class Celery(BaseCelery):
    def on_configure(self):
        client = raven.Client(os.environ.get('SENTRY_DSN'))
        register_logger_signal(client)
        register_signal(client)


def make_celery(app):
    celery = Celery(app.import_name, broker=app.config['CELERY_BROKER_URL'])
    celery.conf.update(app.config)
    TaskBase = celery.Task

    class ContextTask(TaskBase):
        abstract = True

        def __call__(self, *args, **kwargs):
            with app.test_request_context():
                return TaskBase.__call__(self, *args, **kwargs)

    celery.Task = ContextTask

    celery.autodiscover_tasks(
        [app.name] + list(app.blueprints.keys()),
        related_name='tasks')
    return celery


celery = make_celery(hotel.create_application())
task = celery.task

__all__ = ('task',)
