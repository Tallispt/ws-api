from flask import Blueprint, make_response, jsonify, Response
from http import HTTPStatus
from functools import partial

from ..services import data
from ..middlewares.authorization import token_required
from ..middlewares.validation import validate_body
from ..schemas.data import DetectSchema, DataBodySchema

validate_detection = partial(validate_body, schema = DetectSchema)
validate = partial(validate_body, schema = DataBodySchema)

data_bp = Blueprint("data", __name__, url_prefix="/data")

@data_bp.route('/detect', methods=['GET', 'POST'])
@token_required
@validate_detection
def detect_data():
    try:
        response = data.detect_sensor()
        return response, HTTPStatus.OK
        
    except Exception as e:
        print(e)
        return {'error': str(e)}, HTTPStatus.BAD_REQUEST

@data_bp.route('/<id>', methods=['GET'])
@token_required
def get_data(id):
    try:
        response = data.find_data(id)
        return response, HTTPStatus.OK
    
    except Exception as e:
        return {'error': str(e)}, HTTPStatus.BAD_REQUEST

@data_bp.route('', methods=['GET'])
@token_required
def get_user_data():
    try:
        response = data.find_user_data()
        return response, HTTPStatus.OK
    
    except Exception as e:
        return {'error': str(e)}, HTTPStatus.BAD_REQUEST
    
@data_bp.route('', methods=['POST'])
@token_required
@validate
def post_data():
    try:
        response = data.create_data()
        return response, HTTPStatus.CREATED
    
    except Exception as e:
        return {'error': str(e)}, HTTPStatus.BAD_REQUEST
    
@data_bp.route('/<id>', methods=['PUT'])
@token_required
@validate
def put_data(id):
    try:
        response = data.update_data(id)
        return response, HTTPStatus.OK
    
    except Exception as e:
        return {'error': str(e)}, HTTPStatus.BAD_REQUEST
    
@data_bp.route('/<id>', methods=['DELETE'])
@token_required
def delete_data(id):
    try:
        response = data.remove_data(id)
        return response, HTTPStatus.OK
    
    except Exception as e:
        return {'error': str(e)}, HTTPStatus.BAD_REQUEST