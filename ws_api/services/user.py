import bcrypt
# from uuid import uuid4
from flask import request

from ..utils.decode import parse_bytes, parse_json
from ..repositories import user

def create_user():
    user_data = request.json
    username, email, password = user_data.values()

    # # TODO Validate username and password
    # # https://stackoverflow.com/questions/61644396/flask-how-to-make-validation-on-request-json-and-json-schema
    
    existing_user = user.find_by_username(username)
    existing_email = user.find_by_email(email)
    if(existing_user or existing_email):
        raise Exception ("Conflict_error")

    hash = bcrypt.hashpw(parse_bytes(password), bcrypt.gensalt())

    user.insert(username, email, hash.decode('utf-8'))

    response = {"username": username}
    return response