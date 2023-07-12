from flask import request

from ..utils.decode import encode_password
from ..repositories import user

def create_user():
    username, email, password = request.json.values()

    user_or_email_exists(username, email)

    hash = encode_password(password)

    user.insert(username, email, hash)

    return {"username": username}

def user_or_email_exists(username, email):
    db_user = user.find_by_username(username)
    db_email = user.find_by_email(email)
    if(db_user or db_email):
        raise Exception ("Conflict_error")