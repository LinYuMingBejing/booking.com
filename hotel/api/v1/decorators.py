# -*- coding: utf-8 -*- 
from __future__ import absolute_import, division, unicode_literals, print_function

import datetime
import decorator
import jwt
from flask import current_app, request, jsonify, g

from hotel.api.utils import authorization


def authenticated(leeway=None):
    """
    authentication
    """

    def _authenticated(f, *args, **kwargs):
        scheme, token = authorization()
        if scheme not in ['bearer']:
            return jsonify(
                {'code': 'invalid_header', 'description': 'Authorization header must start with Bearer'}), 401

        options = {
            'verify_aud': False
        }
        payload = jwt.decode(
            token,
            current_app.config['SECRET_KEY'],
            options=options,
            leeway=leeway if leeway is not None else datetime.timedelta(seconds=4).total_seconds(),
        )
        g.payload = payload
        return f(*args, **kwargs)

    return decorator.decorator(_authenticated)
