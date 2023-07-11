from functools import wraps
from http import HTTPStatus
from flask import request

from ..services.session import auth_session

def token_required(func):
    @wraps(func)
    def decorated(*args, **kwargs):
        token = request.headers["Authorization"].split(" ")[1]
        
        try:
            auth_session(token)
            return func(*args, **kwargs)
        except Exception as e: 
            return {'error': str(e)}, HTTPStatus.UNAUTHORIZED
        
    return decorated
