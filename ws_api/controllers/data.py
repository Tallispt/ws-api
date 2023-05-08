from flask import Blueprint
from http import HTTPStatus

from ..services import data

data_bp = Blueprint("data", __name__, url_prefix="/data")

@data_bp.route('', methods=['GET'])
def get_data():
    try:
        response = data.find_data()
        return response, HTTPStatus.CONTINUE
    
    except Exception as e:
        return {'error': str(e)}, HTTPStatus.BAD_REQUEST

@data_bp.route('', methods=['POST'])
def post_data():
    try:
        response = data.create_data()
        return response, HTTPStatus.CONTINUE
    
    except Exception as e:
        return {'error': str(e)}, HTTPStatus.BAD_REQUEST