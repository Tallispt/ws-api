from flask import Blueprint
from http import HTTPStatus

from ..services import data
from ..middlewares.authorization import token_required

data_bp = Blueprint("data", __name__, url_prefix="/data")

@data_bp.route('', methods=['GET'])
@token_required
def get_data():
    try:
        response = data.find_data()
        return response, HTTPStatus.OK
    
    except Exception as e:
        return {'error': str(e)}, HTTPStatus.BAD_REQUEST

@data_bp.route('', methods=['POST'])
@token_required
def post_data():
    try:
        response = data.create_data()
        return response, HTTPStatus.CREATED
    
    except Exception as e:
        return {'error': str(e)}, HTTPStatus.BAD_REQUEST