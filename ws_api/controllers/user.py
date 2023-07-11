from flask import Blueprint
from http import HTTPStatus
from marshmallow import ValidationError

from ..services.user import create_user

user_bp = Blueprint("users", __name__, url_prefix="/user")

@user_bp.route('', methods=['POST'])
def post_user():
  try:
    response = create_user()
    return response, HTTPStatus.OK
    
  except Exception or ValidationError as e:
      if(type(e) == ValidationError):
        return {'error': str(e)}, HTTPStatus.FORBIDDEN
      
      if(str(e) == 'Conflict_error'):
        return {'error': "User already exists!"}, HTTPStatus.CONFLICT
      return {'error': str(e)}, HTTPStatus.BAD_REQUEST