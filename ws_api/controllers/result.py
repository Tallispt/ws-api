from flask import Blueprint
from http import HTTPStatus
from functools import partial

from ..services import result
from ..middlewares.authorization import token_required
from ..middlewares.validation import validate_body
from ..schemas.data import DataBodySchema

validate = partial(validate_body, schema = DataBodySchema)

result_bp = Blueprint("result", __name__, url_prefix="/result")

@result_bp.route('', methods=['GET'])
@token_required
def get_results():
  try:
    response = result.find_all_results()
    return response, HTTPStatus.OK
    
  except Exception as e:
      return {'error': str(e)}, HTTPStatus.BAD_REQUEST
  
@result_bp.route('/<id>', methods=['GET'])
@token_required
def find_result(id):
  try:
    response = result.find_result(id)
    return response, HTTPStatus.OK
    
  except Exception as e:
    if(str(e) == 'Not_found_error'):
      return {'error': "Result not found!"}, HTTPStatus.NOT_FOUND
    return {'error': str(e)}, HTTPStatus.BAD_REQUEST
  
@result_bp.route('/<id>', methods=['PUT'])
@token_required
@validate
def put_result(id):
  try:
      response = result.update_result(id)
      return response, HTTPStatus.OK
  
  except Exception as e:
      return {'error': str(e)}, HTTPStatus.BAD_REQUEST
    
@result_bp.route('/<id>', methods=['DELETE'])
@token_required
def delete_result(id):
  try:
    response = result.remove_result(id)
    return response, HTTPStatus.OK
  
  except Exception as e:
    if(str(e) == "'NoneType' object is not subscriptable"):
        return {'error': "Result not found!"}, HTTPStatus.NOT_FOUND
    return {'error': str(e)}, HTTPStatus.BAD_REQUEST