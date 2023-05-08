from flask_httpauth import HTTPTokenAuth
from werkzeug.security import generate_password_hash, check_password_hash

token_auth = HTTPTokenAuth(scheme='Bearer')

allowed = {
    "tallis": generate_password_hash('my_pass')
}

@token_auth.verify_token
def verify_token(token):
    if token not in allowed:
        return None
    
    return allowed[token]
