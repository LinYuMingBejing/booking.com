# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, unicode_literals, print_function

from hotel import redis_store, celery
from hotel.models import Hotel
from celery.signals import worker_ready
import json


@worker_ready.connect()
def on_worker_init(**_):
    pass


@celery.task(bind=True)
def update_page(task, pages):
    for p in pages:
        try:
            hotel = p['hotel']
            try:
                hotel = Hotel.objects.get(page_id=hotel)
            except Hotel.DoesNotExist:
                hotel = Hotel()
                hotel.hotel = p['hotel']
            hotel.page_url = p['page_url']
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
            hotel.save()
        
        except Exception as ex:
            logger.error(p)
            logger.error(ex, exc_info=True)
    

        
@celery.task(bind=True)
def clear_cache(task):
    redis_store.flushdb()

