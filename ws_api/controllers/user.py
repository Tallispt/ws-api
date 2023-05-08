from flask import Blueprint, request
from http import HTTPStatus

from ..services.user import create_user

user_bp = Blueprint("users", __name__, url_prefix="/user")

@user_bp.route('', methods=['POST'])
def post_user():
  
  try:
    response = create_user()
    return response, HTTPStatus.CREATED
  
  except Exception as e:
    if(str(e) == 'Conflict_error'):
      return {'error': "User already exists!"}, HTTPStatus.CONFLICT
    
    return {'error': str(e)}, HTTPStatus.BAD_REQUEST