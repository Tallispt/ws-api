from http import HTTPStatus
from flask import Blueprint
from marshmallow import ValidationError

from ..services import session

session_bp = Blueprint('session', __name__, url_prefix='/session')

@session_bp.route('', methods=['POST'])
# @validation(SignInSchema)
def post_session():

    try:
        response = session.create_session()
        return response, HTTPStatus.OK
    
    except Exception or ValidationError as e:
      
      if(type(e) == ValidationError):
        return {'error': str(e)}, HTTPStatus.FORBIDDEN
      
      if(str(e) == 'Login_error'):
          return {'error': "Unauthorazed access!"}, HTTPStatus.UNAUTHORIZED
      return {'errrr': str(e)}, HTTPStatus.BAD_REQUEST
    
@session_bp.route('', methods=['DELETE'])
def delete_session():

    try:
        session.delete()
        return {}, HTTPStatus.OK
    
    except Exception as e:
      return {'error': str(e)}, HTTPStatus.BAD_REQUEST