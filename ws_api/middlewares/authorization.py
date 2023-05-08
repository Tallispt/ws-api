from flask_httpauth import HTTPTokenAuth

from ..repositories import session
from ..utils.decode import parse_json

token_auth = HTTPTokenAuth(scheme='Bearer')

@token_auth.verify_token
def verify_token(token):
    user = session.find_by_token(token)
    if(user and user['is_valid']):
        print(user['is_valid'])
        return {'user'}
    return None