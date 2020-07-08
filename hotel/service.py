# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, unicode_literals, print_function

import json
import logging
from urllib.parse import urlparse
from mongoengine.queryset.visitor import Q
from hotel.models import Hotel


def to_dict(data):
    page = {}
    page['page_url'] = data['page_url']
    page['hotel'] = data['hotel']
    page['ratings'] = data['ratings']
    page['description'] = data['description']
    page['facilities'] = data['facilities']
    page['comments'] = data['comments']
    page['photo'] = data['photo']
    page = {k: v for k, v in page.items() if v }
    return page


@cache.memoize(CACHE_TIMEOUT)
def find_by_hotel(hotel):
    pages = []
    try:
        pages = Hotel.objects.get(hotel=hotel)
        pages = list(map(to_dict, pages))
    except Hotel.DoesNotExist:
        logger.warning('not exist. hotel=%s', hotel)

    return pages


@cache.memoize(CACHE_TIMEOUT)
def find_by_ratings(address, high_ratings:int, low_ratings:int):
    pages = []
    try:
        pages = Hotel.objects(Q(address=address) & \
                            Q(ratings__lte=high_ratings) & \
                            Q(ratings__get=low_ratings))
        pages = list(map(to_dict, pages))

    except Hotel.DoesNotExist:
        logger.warning('not exist. address=%s ratings=%s', address, ratings)

    return pages


@cache.memoize(CACHE_TIMEOUT)
def find_by_stars(address, high_stars:int, low_stars:int):
    pages = []
    try:
        pages = Hotel.objects(Q(address=address) & \
                            Q(stars__lte=high_stars) & \
                            Q(stars__get=low_stars))
        pages = list(map(to_dict, pages))

    except Hotel.DoesNotExist:
        logger.warning('not exist. address=%s ratings=%s', address, ratings)

    return pages