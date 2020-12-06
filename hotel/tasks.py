# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, unicode_literals, print_function

from celery.signals import worker_ready
import celery
from concurrent.futures import ThreadPoolExecutor, as_completed
from datetime import datetime

from hotel.models import HotelInfo
from hotel.crawler import CrawlerManager


UPLOAD_COUNT = 5000


class Task(celery.Task):
    def on_failure(self, exc, task_id, args, kwargs, einfo):
        print('{0!r} failed: {1!r}'.format(task_id, exc))

    def on_success(self, retval, task_id, args, kwargs):
        pass

    def on_retry(self, exc, task_id, args, kwargs, einfo):
        pass


@worker_ready.connect()
def on_worker_init(**_):
    pass


from hotel import redis_store, celery


@celery.task(bind=False, base=Task)
def clear_cache():
    redis_store.flushdb()


@celery.task(ignore_result=True)
def crawler():
    crawlerManager = CrawlerManager('https://www.booking.com/searchresults.zh-tw.html?city=-2637882&dest_id=-2637882&dest_type=city&offset=75')
    
    hotelPages = crawlerManager.crawlHotelPage()
    for pages in hotelPages:
        with ThreadPoolExecutor(max_workers = 5) as pool:
            futures = [pool.submit(crawlerManager.parse, url) for url in pages]


@celery.task(bind=False, base=Task)
def upload(rows):
    pages = []
    if not isinstance(rows, list):
        upsert([update_page(rows)])
        return

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
