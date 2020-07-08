# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, unicode_literals, print_function

from flask import request
from . import errors
import re


def authorization():
    """
    Retrieves the Authorization header and parses it into scheme and token
    """
    scheme = None
    token = None
    try:
        if "Authorization" in request.headers:
            scheme, token = request.headers['Authorization'].split(' ', 1)
        if "authorization" in request.headers:
            scheme, token = request.headers['authorization'].split(' ', 1)
    except KeyError:
        raise errors.AuthenticationMissing()
    except ValueError:
        raise errors.AuthenticationInvalid()
    if not scheme:
        raise errors.AuthenticationMissing()
    if not token:
        raise errors.AuthenticationInvalid()
    return scheme.lower(), token