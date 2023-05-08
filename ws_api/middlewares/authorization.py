from flask_httpauth import HTTPTokenAuth
from werkzeug.security import generate_password_hash, check_password_hash
from ..repositories import session

token_auth = HTTPTokenAuth(scheme='Bearer')

@token_auth.verify_token
def verify_token(token):
    user = session.find_by_token(token)
    if(user['is_valid']):
        return user
