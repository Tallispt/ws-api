from http import HTTPStatus
from flask import Blueprint

from ..services import session

session_bp = Blueprint('session', __name__, url_prefix='/session')

@session_bp.route('', methods=['POST'])
def post_session():
    
    try:
        response = session.create_session()
        return response, HTTPStatus.CONTINUE
    
    except Exception as e:
        return {'error': str(e)}, HTTPStatus.BAD_REQUEST

@session_bp.route('', methods=['GET'])
def get_session():
    
    try:
        response = session.login()
        return response, HTTPStatus.OK
    
    except Exception as e:
      if(str(e) == 'Login_error'):
          return {'error': "Unauthorazed access!"}, HTTPStatus.UNAUTHORIZED
      return {'error': str(e)}, HTTPStatus.BAD_REQUEST