# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, unicode_literals, print_function

import os
import random


DEBUG = False
TESTING = False
SECRET_KEY = os.environ.get(
    'SECRET_KEY', '{:030x}'.format(random.randrange(16 ** 30)))
SERVER_NAME = os.environ.get('SERVER_NAME')


DATE_FORMAT = '%Y-%m-%dT%H:%M:%S'
