# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, unicode_literals, print_function

import jwt
from flask import current_app, request, jsonify
from flask_cors import cross_origin

from hotel import service
from hotel.api.v1 import application as app
from hotel.api.v1.decorators import authenticated


@app.route('/hotel/name', methods=['GET'])
@authenticated()
@cross_origin()
def hotel():
    try:
        result = {"status": True}
        hotel = request.args.get("hotel")
        result['data'] = service.find_by_hotel(hotel)
    except Exception as e:
        result["status"] = False
        result['error'] = e
    
    return jsonify(result)


@app.route('/hotel/rating', methods=['GET'])
@authenticated()
@cross_origin()
def hotel_rating():
    try:
        result = {"status": True}
        address = request.args.get("address")
        high_rating = request.args.get("high_rating")
        low_rating = request.args.get("low_rating")
        result['data'] = service.find_by_ratings(address, high_rating, low_rating)

    except Exception as e:
        result["status"] = False
        result['error'] = e
    
    return jsonify(result)


@app.route('/hotel/stars', methods=['GET'])
@authenticated()
@cross_origin()
def hotel_star():
    try:
        result = {"status": True}
        address = request.args.get("address")
        high_stars = request.args.get("high_stars")
        low_stars = request.args.get("low_stars")
        result['data'] = service.find_by_stars(address, high_stars, low_stars)

    except Exception as e:
        result["status"] = False
        result['error'] = e
    
    return jsonify(result)


@app.route('/update/url', methods=['POST'])
@authenticated()
def update():
    res = {"status": True}
    try:
        from hotel.tasks import update_page
        pages = request.json        
        update_page.delay(pages)
        res["msg"] = "success"

    except Exception as e:
        res["status"] = False
        res["msg"] = "fail {}".format(e)
    
    return jsonify(res)