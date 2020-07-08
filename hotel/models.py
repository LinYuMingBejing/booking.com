# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, unicode_literals, print_function

from datetime import datetime
from hotel import mongo as db


class Hotel():
    page_url = db.StringField()
    hotel = db.StringField()
    address = db.StringField()
    city = db.StringField()
    town = db.StringField()
    ratings = db.IntField(default=0)
    description = db.StringField()
    facilities = db.ListField()
    bed_type = db.ListField()
    stars = db.IntField(default=0)
    comments = db.ListField()
    tourists = db.ListField()
    photo = db.ListField()
    meta = {
        'indexes': [
            'hotel',
            ('address', 'ratings',),
            ('address','stars',)
        ]
    }


    def save(self, *args, **kwargs):
        if not self.creation_date:
            self.creation_date = datetime.datetime.now()
        self.modified_date = datetime.datetime.now()
        return super(Page, self).save(*args, **kwargs)

    def __unicode__(self):
        return self.url

    def __repr__(self):
        return '<Page {page.page_id}>'.format(page=self)

    def to_dict(self):
        return {
            "page_url": self.page_url,
            "hotel": self.hotel,
            "address": self.address,
            "city": self.city,
            "town": self.town,
            "ratings": self.ratings,
            "description": self.description,
            "facilities": self.facilities,
            "bed_type": self.bed_type,
            'stars': self.stars,
            "comments":self.comments,
            "tourists":self.tourists,
            "photo":self.photo,
            "creation_date": self.creation_date,
            "modified_date": self.modified_date
        }    