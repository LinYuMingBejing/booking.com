# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, unicode_literals, print_function

from hotel import redis_store, celery
from hotel.models import HotelInfo
from celery.signals import worker_ready
from datetime import datetime
import json


UPLOAD_COUNT = 5000


@worker_ready.connect()
def on_worker_init(**_):
    pass


@celery.task(bind=True)
def clear_cache(task):
    redis_store.flushdb()


@celery.task(bind=True)
def upload(task, rows):
    pages = []
    if not isinstance(rows, list):
        upsert([update_page(rows)])
        return

    rows = json.loads(rows)
    for row in rows:
        instance = update_page(row)
        pages.append(instance)

        if len(pages) >= UPLOAD_COUNT:
            upsert(pages)
            pages = []

    upsert(pages)


def update_page(page):
    now = datetime.now()
    pageUrl = page.get('pageUrl')

    try:
        hotel = HotelInfo.objects.get(pageUrl = pageUrl)
    except HotelInfo.DoesNotExist:
        hotel = HotelInfo()
        hotel.pageUrl = pageUrl
        hotel.creation_date = now

    hotel.hotel = page.get('hotel', '')
    hotel.address = page.get('address', '')
    hotel.city = page.get('city', '')
    hotel.town = page.get('town', '')
    hotel.ratings = page.get('ratings', 0)
    hotel.description = page.get('description', '')
    hotel.facilities = page.get('facilities', '')
    hotel.bed_type = page.get('bed_type', '')
    hotel.stars = page.get('stars', 0)
    hotel.comments = page.get('comments', None)
    hotel.tourists = page.get('tourists', '')
    hotel.photo = page.get('photo', '')
    hotel.modified_date = now
    return hotel        
    

def upsert(pages):
    bulk = HotelInfo._get_collection().initialize_ordered_bulk_op()
    for page in pages:
        bulk.find({'pageUrl': page['pageUrl']}).upsert().replace_one(page.to_mongo())
    bulk.execute()
