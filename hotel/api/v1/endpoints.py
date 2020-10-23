# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, unicode_literals, print_function

import jwt
from flask import current_app, request, jsonify, Response
from flask_cors import cross_origin

from hotel import service
from hotel.api.v1 import application as app
from hotel.api.v1.decorators import authenticated

import prometheus_client
from prometheus_client import Counter, Gauge
import requests
import prometheus_client
from prometheus_client.core import CollectorRegistry
from prometheus_client import Counter
from flask import Response


# Http的請求總數
total_requests = Counter('request_count', 'Total webapp request count')


@app.route('/metrics')
@cross_origin()
def requests_count():
    total_requests.inc()
    return Response(prometheus_client.generate_latest(), mimetype='text/plain')


@app.route('/')
def index():
    total_requests.inc()
    return jsonify({
        'status': 'ok',
        'msg':'Hello world!'
    })


@app.route('/hotel/name', methods=['GET'])
@cross_origin()
def hotel():
    total_requests.inc()
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
    total_requests.inc()
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
    total_requests.inc()
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
    total_requests.inc()
    res = {'status': True}
    try:
        from hotel.tasks import upload
        pages = request.json        
        upload.delay(pages)
        res['msg'] = 'success'

    except Exception as e:
        res['status'] = False
        res['msg'] = 'fail {}'.format(e)
    
    return jsonify(res)