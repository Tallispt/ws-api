from flask import Blueprint
from http import HTTPStatus
from functools import partial

from ..services.user import create_user
from ..middlewares.validation import validate_body
from ..schemas.user import SignUpSchema

user_bp = Blueprint("users", __name__, url_prefix="/user")

validate = partial(validate_body, schema = SignUpSchema)

@user_bp.route('', methods=['POST'])
@validate
def post_user():
  try:
    response = create_user()
    return response, HTTPStatus.OK
    
  except Exception as e:
      if(str(e) == 'Conflict_error'):
        return {'error': "User already exists!"}, HTTPStatus.CONFLICT
      
      print(e)
      
      return {'error': str(e)}, HTTPStatus.BAD_REQUEST