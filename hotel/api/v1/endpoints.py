# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, unicode_literals, print_function

import jwt
from flask import current_app, request, jsonify, Response
from flask_restplus import Resource, fields

from hotel import service
from hotel.api.v1 import api, app
from hotel.api.v1.decorators import authenticated


@app.after_request
def after_request(response):
    response.headers.add('Access-Control-Allow-Origin', '*')
    return response


api = api.namespace('booking', description='Simple API (version 1)')

form = api.model('data',{
    'pageUrl': fields.Url(description='pageUrl', required=True),
    'hotel': fields.String(description='hotel name', required=True),
    'address': fields.String(description='address', required=True),
    'city': fields.Integer(description='city', required=True),
    'town': fields.String(description='town', required=True),
    'ratings': fields.Float(description='description', required=True),
    'facilities': fields.List(cls_or_instance = fields.String, description='facilities', required=True),
    'bed_type': fields.List(cls_or_instance = fields.String, description='bed_type', required=True),
    'stars': fields.Float(description = 'stars', required=True),
    'tourists': fields.List(cls_or_instance = fields.String, description='tourists', required=True),
    'comments': fields.List(cls_or_instance = fields.String, description='comments', required=True),
    'photo': fields.List(cls_or_instance = fields.String, description='photo', required=True)
    }
)


@api.route('/index', methods=['GET'])
class index(Resource):
    def get(self):
        return jsonify({
            'status': True,
            'msg':'Hello world!'
        })


@api.route('/hotel/name', methods=['GET'])
@api.doc(params={'name': 'Hotel name'})
class name(Resource):
    def get(self):
        res = {'status': False}
        data = request.args.to_dict()
        if 'name' not in data:
            res['msg'] = 'Lack of required parameters'
            return jsonify(res), 401
        
        try:
            res.update({
                'status': True,
                'data' :service.find_by_hotel(data['name'])
            })
        except Exception as e:
            res['msg'] = e
        return jsonify(res)


@api.route('/hotel/ratings', methods=['GET'])
@api.doc(params={'city': 'city name. ex: 台北', 'high_rating':'ex:10', 'low_rating':'ex:1'})
class ratings(Resource):
    def get(self):
        res = {'status': False}
        data = request.args.to_dict()

        if 'city' not in data or 'high_rating' not in data or 'low_rating' not in data:
            res['msg'] = 'Lack of required parameters'
            return jsonify(res), 401

        try:
            res.update({
                'status': True,
                'data' :service.find_by_ratings(data['city'], data['high_rating'], data['low_rating'])
            })

        except Exception as e:
            res['msg'] = e
    
        return jsonify(res)


@api.route('/hotel/stars', methods=['GET'])
@api.doc(params={'city': 'city name. ex: 台北', 'high_star':'ex:10', 'low_star':'ex:1'})
class start(Resource):
    def get(self):
        res = {'status': False}
        
        try:
            data = request.args.to_dict()

            if 'city' not in data or 'high_star' not in data or 'high_star' not in data:
                res['msg'] = 'Lack of required parameters'
                return jsonify(res), 401

            res.update({
                'status': True,
                'data' :service.find_by_stars(data['city'], data['high_stars'], data['low_stars'])
            })

        except Exception as e:
            res['error'] = e

        return jsonify(res)


@api.route('/hotel/update', methods=['POST'])
class update(Resource):
    @api.doc(body=form)
    def post(self):
        res = {'status': True}
        try:
            from hotel.tasks import upload
            pages = request.data
            upload.delay(pages)

        except Exception as e:
            res['status'] = False
            res['msg'] = 'fail {}'.format(e)
        
        return jsonify(res)
