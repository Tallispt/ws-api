from functools import wraps
from http import HTTPStatus
from flask import request

from ..services.session import auth_session

def token_required(func):
    @wraps(func)
    def decorated(*args, **kwargs):
        try:
            token = request.headers["Authorization"].split(" ")[1]  
            if(not token):
                raise Exception
            user_id = auth_session(token)
            request.environ['user_id'] = user_id

            return func(*args, **kwargs)
        except Exception as e: 
            return {'error': str(e)}, HTTPStatus.UNAUTHORIZED
        
    return decorated
