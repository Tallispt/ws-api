from flask import Blueprint
from http import HTTPStatus
from functools import partial

from ..services import mode
from ..middlewares.authorization import token_required
from ..middlewares.validation import validate_body
from ..schemas.mode import ModeBodySchema

validate = partial(validate_body, schema = ModeBodySchema)

mode_bp = Blueprint("mode", __name__, url_prefix="/mode")

@mode_bp.route('', methods=['GET'])
@token_required
def get_modes():
  try:
    response = mode.find_user_modes()
    return response, HTTPStatus.OK
    
  except Exception as e:
      return {'error': str(e)}, HTTPStatus.BAD_REQUEST
  
@mode_bp.route('/<id>', methods=['GET'])
@token_required
def get_mode_by_id(id):
  try:
    response = mode.find_mode(id)
    return response, HTTPStatus.OK
    
  except Exception as e:
    return {'error': str(e)}, HTTPStatus.BAD_REQUEST
  
@mode_bp.route('', methods=['POST'])
@token_required
@validate
def post_modes():
  try:
    response = mode.create_mode()
    return response, HTTPStatus.CREATED
    
  except Exception as e:
    if(str(e) == 'Conflict_error'):
      return {'error': "Mode already exists!"}, HTTPStatus.CONFLICT
    return {'error': str(e)}, HTTPStatus.BAD_REQUEST
  
@mode_bp.route('/<id>', methods=['PUT'])
@token_required
@validate
def put_modes(id):
  try:
    response = mode.update_mode(id)
    return response, HTTPStatus.OK
    
  except Exception as e:
    return {'error': str(e)}, HTTPStatus.BAD_REQUEST
  
@mode_bp.route('/<id>', methods=['DELETE'])
@token_required
def delete_modes(id):
  try:
    response = mode.remove_mode(id)
    return response, HTTPStatus.OK
    
  except Exception as e:
    return {'error': str(e)}, HTTPStatus.BAD_REQUEST