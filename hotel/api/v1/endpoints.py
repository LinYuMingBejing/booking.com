# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, unicode_literals, print_function

import jwt
from flask import current_app, request, jsonify
from flask_cors import cross_origin

from hotel import service
from hotel.api.v1 import application as app
from hotel.api.v1.decorators import authenticated


@app.route('/hotel/name', methods=['GET'])
@cross_origin()
def hotel():
    result = {'msg': '', 'status': False}
    data = request.args
    if 'hotel' not in data:
        result['msg'] = 'Lack of required parameters'
        return jsonify(result), 401
    try:
        hotel = data.get('hotel',None)
        result.update({
            'msg': 'ok',
            'status': True,
            'data' :service.find_by_hotel(hotel)
        })
    except Exception as e:
        result['msg'] = e
    return jsonify(result)


@app.route('/hotel/rating', methods=['GET'])
@cross_origin()
def hotel_rating():
    result = {'msg': '', 'status': False}
    data = request.args
    if 'city' not in data or 'high_rating' not in data or 'low_rating' not in data:
        result['msg'] = 'Lack of required parameters'
        return jsonify(result), 401
    try:
        city = data.get('city',None)
        high_rating = data.get('high_rating',None)
        low_rating = data.get('low_rating',None)
        result.update({
            'msg': 'ok',
            'status': True,
            'data' :service.find_by_ratings(city, high_rating, low_rating)
        })

    except Exception as e:
        result['msg'] = e
    
    return jsonify(result)


@app.route('/hotel/stars', methods=['GET'])
@cross_origin()
def hotel_star():
    result = {'msg': '', 'status': False}
    data = request.args
    if 'city' not in data or 'high_star' not in data or 'low_star' not in data:
        result['msg'] = 'Lack of required parameters'
        return jsonify(result), 401
    try:
        city = data.get('city', None)
        high_stars = data.get('high_star', None)
        low_stars = data.get('low_star', None)
        result.update({
            'msg': 'ok',
            'status': True,
            'data' :service.find_by_stars(city, high_stars, low_stars)
        })

    except Exception as e:
        result['error'] = e

    return jsonify(result)


@app.route('/update/url', methods=['POST'])
@authenticated()
def update():
    res = {'status': True}
    try:
        from hotel.tasks import update_page
        pages = request.json        
        update_page.delay(pages)
        res["msg"] = "success"

    except Exception as e:
        res["status"] = False
        res["msg"] = "fail {}".format(e)
    
    return jsonify(res)