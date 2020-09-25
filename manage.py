#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, unicode_literals, print_function

import flask_script as script
from prometheus_flask_exporter.multiprocess import UWsgiPrometheusMetrics

import hotel

app = hotel.create_application()

manager = script.Manager(app)
manager.add_command('runserver', script.Server(host='0.0.0.0', port=8000))
manager.add_command('shell', script.Shell(make_context=lambda: {
    'current_app': app
}))

metrics = UWsgiPrometheusMetrics(app=app, default_labels={'project': 'hotel'})
metrics.start_http_server(9200)


if __name__ == "__main__":
    manager.run()
