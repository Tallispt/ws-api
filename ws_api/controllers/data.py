from flask import Blueprint
from http import HTTPStatus
from functools import partial

from ..services import data
from ..middlewares.authorization import token_required
from ..middlewares.validation import validate_body, validate_file, validate_form
from ..schemas.data import DetectFormsBodySchema, DetectDelBodySchema, DataBodySchema

validate_detection_file = partial(validate_file)
validate_detection_form = partial(validate_form, schema = DetectFormsBodySchema)
validate_detection_delete = partial(validate_body, schema = DetectDelBodySchema)
validate = partial(validate_body, schema = DataBodySchema)

data_bp = Blueprint("data", __name__, url_prefix="/data")

@data_bp.route('/detect', methods=['GET', 'POST'])
@token_required
@validate_detection_file
@validate_detection_form
def detect_data():
    try:
        response = data.detect_sensor()
        return response, HTTPStatus.OK
        
    except Exception as e:
        return {'error': str(e)}, HTTPStatus.BAD_REQUEST
    
@data_bp.route('/detect', methods=['DELETE'])
@token_required
@validate_detection_delete
def delete_detect_data():
    try:
        response = data.delete_sensor()
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
        if(str(e) == 'Mode_error'):
            return {'error': "Mode does not exist!"}, HTTPStatus.FORBIDDEN
        return {'error': str(e)}, HTTPStatus.BAD_REQUEST