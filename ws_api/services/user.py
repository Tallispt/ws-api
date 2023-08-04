from flask import request

from ..utils.decode import encode_password
from ..repositories import user, mode
from ..seed.mode_seed import Default_regression_mode

def create_user():
    username, email, password = request.json.values()

    user_or_email_exists(username, email)

    hash = encode_password(password)

    created_user = user.insert(username, email, hash)

    # mode.insert(Default_regression_mode, created_user.inserted_id)

    return {"username": username}

def user_or_email_exists(username, email):
    db_user = user.find_by_username(username)
    db_email = user.find_by_email(email)
    if(db_user or db_email):
        raise Exception ("Conflict_error")