# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, unicode_literals, print_function


class AuthenticationInvalid(Exception):
    pass


class AuthenticationMissing(Exception):
    pass


class MissingRequiredScopes(Exception):
    pass


class RegisterRepeated(Exception):
    pass


class NotDomainOwner(Exception):
    pass
