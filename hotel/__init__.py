# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, unicode_literals, print_function

import logging
import os
import urllib
from logging.config import dictConfig

from flask import Flask
from flask_caching import Cache
from flask_mongoengine import MongoEngine
from flask_redis import FlaskRedis

from hotel.settings.defaults import LOG_FILE_PATH, ERROR_LOG_FILE_PATH


mongo = MongoEngine()
redis_store = FlaskRedis(decode_responses=True)

__version__ = '1.0.0'
__all__ = ('cache', 'caches', 'db')

caches = {
    'default': Cache(),
}

cache = caches['default']

def create_application(settings=None):
    raven_logger = logging.getLogger('raven.base.Client')
    raven_logger.setLevel(logging.CRITICAL)
    dictConfig({
        'version': 1,
        'formatters': {'default': {
            'format': '[%(asctime)s][%(levelname)s][%(process)s][%(filename)s:%(lineno)d] %(message)s',
        }},
        'handlers': {
            'default': {
                'class': 'logging.StreamHandler',
                'formatter': 'default'
            },
            'file': {
                'formatter': 'default',
                'class': 'logging.handlers.TimedRotatingFileHandler',
                'filename': LOG_FILE_PATH,
                'when': 'midnight'
            },
            'error': {
                'formatter': 'default',
                'class': 'logging.handlers.TimedRotatingFileHandler',
                'level': 'ERROR',
                'filename': ERROR_LOG_FILE_PATH,
                'when': 'midnight'
            }
        },
        'root': {
            'level': 'INFO',
            'handlers': ['default', 'file', 'error']
        }
    })

    app = Flask('hotel', static_folder="../static")
    app.config.from_object('hotel.settings.defaults')
    if os.environ.get('SETTINGS_MODULE'):
        app.config.from_object(os.environ.get('SETTINGS_MODULE'))
    if settings is not None:
        if isinstance(settings, dict):
            app.config.update(settings)
        else:
            app.config.from_object(settings)
    
    def init_caches(app, caches):
        for name, cache in caches.items():
            def config():
                uri = urllib.parse.urlparse(
                    os.environ.get('CACHE_URL_{name}'.format(name=name).upper(), 'null://')
                )
                query = dict(urllib.parse.parse_qsl(uri.query))

                yield 'CACHE_TYPE', uri.scheme
                if 'timeout' in query:
                    yield 'CACHE_DEFAULT_TIMEOUT', int(query['timeout'])
                if 'threshold' in query:
                    yield 'CACHE_THRESHOLD', int(query['threshold'])
                # yield 'CACHE_ARGS',
                # yield 'CACHE_OPTIONS',

                if uri.scheme == 'redis':
                    # yield 'CACHE_REDIS_URL', urllib.parse.urlunparse(uri)
                    yield 'CACHE_REDIS_HOST', uri.hostname
                    if uri.port:
                        yield 'CACHE_REDIS_PORT', uri.port
                    if uri.password:
                        yield 'CACHE_REDIS_PASSWORD', uri.password
                    yield 'CACHE_REDIS_DB', uri.path.lstrip('/')
                elif uri.scheme in ['memcached', 'gaememcached', 'saslmemcached']:
                    yield 'CACHE_MEMCACHED_SERVERS', [uri.netloc]

                    if uri.scheme == 'saslmemcached':
                        if uri.username:
                            yield 'CACHE_MEMCACHED_USERNAME', uri.username
                        if uri.password:
                            yield 'CACHE_MEMCACHED_PASSWORD', uri.password
                elif uri.scheme == 'filesystem':
                    yield 'CACHE_DIR', uri.netloc.hostname + uri.path

            cache.init_app(app, config=dict(config()))

    def init_mongo(app, mongo):
        mongo.init_app(app)

    def init_redis_db(app, redis_store):
        redis_store.init_app(app)

    init_mongo(app, mongo)
    init_caches(app, caches)
    init_redis_db(app, redis_store)

    # Register blueprints
    import hotel.api.v1
    app.register_blueprint(hotel.api.v1.application)

    return app
