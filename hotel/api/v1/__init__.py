# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, unicode_literals, print_function

import logging

import jwt
from flask import Blueprint, jsonify
from flask_restplus import Api

app = application = Blueprint('hotel.v1', __name__)
api = Api(application)


from . import endpoints
from hotel.api.errors import AuthenticationMissing, AuthenticationInvalid, NotDomainOwner

logger = logging.getLogger()

__all__ = ('endpoints', 'errors',)

JWT_ERRORS = {
    jwt.ExpiredSignature: ({'code': 'token_expired', 'description': 'token is expired', 'status': False}, 401),
    jwt.InvalidAudienceError: (
        {'code': 'invalid_audience', 'description': 'incorrect audience, expected: ', 'status': False}, 401),
    jwt.InvalidIssuer: ({'code': 'invalid_issuer', 'description': 'incorrect issuer', 'status': False}, 401),
    jwt.DecodeError: (
        {'code': 'token_invalid_signature', 'description': 'token signature is invalid', 'status': False}, 401)
}


@app.errorhandler(jwt.DecodeError)
@app.errorhandler(jwt.ExpiredSignature)
@app.errorhandler(jwt.InvalidAudienceError)
@app.errorhandler(jwt.InvalidIssuer)
def handle_jwt_errors(error):
    data, code = JWT_ERRORS[error.__class__]
    return jsonify(data), code


@app.errorhandler(AuthenticationMissing)
def handle_auth_missing(error):
    return jsonify({
        'status': False,
        'code': 'authorization_header_missing',
        'description': 'Authorization query is expected'
    }), 401


@app.errorhandler(AuthenticationInvalid)
def handle_auth_invalid(error):
    return jsonify({
        'code': 'authorization_invalid', 'description': 'Token not found',
        'status': False
    }), 401


@app.errorhandler(NotDomainOwner)
def handle_auth_domain_invalid(error):
    return jsonify({
        'code': 'authorization_invalid', 'description': 'Not Domain Owner',
        'status': False
    }), 401


@app.errorhandler(Exception)
def handle_exception(error):
    logger.error(error, exc_info=True)
    return jsonify({
        'code': 'exception', 'description': 'something wrong',
        'status': False
    }), 500

