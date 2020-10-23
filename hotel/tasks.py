# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, unicode_literals, print_function

from hotel import redis_store, celery
from hotel.models import Hotel
from celery.signals import worker_ready
import json
import multiprocessing as mp


UPLOAD_COUNT = 5000

@worker_ready.connect()
def on_worker_init(**_):
    pass


@celery.task(bind=True)
def clear_cache(task):
    redis_store.flushdb()


@celery.task(bind=True)
def upload(task, pages):
    pages = []
    lock = mp.Lock()
    for page in pages:
        instance = update_page(page)
        pages.append(instance)

        if len(pages) >= UPLOAD_COUNT:
            upsert(pages, lock)
            pages = []
    
    upsert(pages, lock)


def update_page(pages):
    now = datetime.now()
    p = json.loads(pages)
    hotel = p.get('page_id')

    try:
        hotel = Hotel.objects.get(page_id=hotel)
    except Hotel.DoesNotExist:
        hotel = Hotel()
        hotel.page_id = page_id
        page.creation_date = now

    hotel.page_url = p.get('page_url', '')
    hotel.address = p.get('address', '')
    hotel.city = p.get('city', '')
    hotel.town = p.get('town', '')
    hotel.ratings = p.get('ratings', 0)
    hotel.description = p.get('description', '')
    hotel.facilities = p.get('facilities', '')
    hotel.bed_type = p.get('bed_type', '')
    hotel.stars = p.get('stars', 0)
    hotel.comments = p.get('comments', None)
    hotel.tourists = p.get('tourists', '')
    hotel.photo = p.get('photo', '')
    hotel.modified_date = now
    return hotel        
    

def upsert(pages, lock):
    lock.acquire()
    if not pages:
        return 
    bulk = Hotel._get_collection().initialize_ordered_bulk_op()
    for page in pages:
        bulk.find({'page_id': page['page_id'] }).upsert().replace_one(page.to_mongo())
    bulk.execute()
    lock.release()