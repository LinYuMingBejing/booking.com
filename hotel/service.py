# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, unicode_literals, print_function

import json
import logging
from urllib.parse import urlparse
from mongoengine.queryset.visitor import Q

from hotel.models import HotelInfo
from hotel import cache

CACHE_TIMEOUT = 60 * 60 * 1
PULL_COUNT = 5

logger = logging.getLogger()


def to_dict(data):
    page = {}
    page['page_url'] = data['pageUrl']
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
        pages = HotelInfo.objects.get(hotel=hotel)
        pages = list(map(to_dict, pages))
    except HotelInfo.DoesNotExist:
        logger.warning('not exist. hotel=%s', hotel)
    return pages


@cache.memoize(CACHE_TIMEOUT)
def find_by_ratings(city, high_ratings:int, low_ratings:int):
    pages = []
    try:
        pages = HotelInfo.objects(Q(city=city)&
                              Q(ratings__gte=low_ratings)&
                              Q(ratings__lte=high_ratings))\
                     .order_by('-ratings')[:PULL_COUNT]
        pages = list(map(to_dict, pages))

    except HotelInfo.DoesNotExist:
        logger.warning('not exist. city=%s ratings=%s', city, ratings)

    return pages


@cache.memoize(CACHE_TIMEOUT)
def find_by_stars(city, high_stars:int, low_stars:int):
    pages = []
    try:
        pages = HotelInfo.objects(Q(city=city) & \
                            Q(stars__lte=high_stars) & \
                            Q(stars__gte=low_stars))\
                     .order_by('-stars')[:PULL_COUNT]
        pages = list(map(to_dict, pages))

    except HotelInfo.DoesNotExist:
        logger.warning('not exist. city=%s ratings=%s', city, ratings)

    return pages