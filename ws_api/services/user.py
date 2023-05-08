from flask import request

from ..utils.decode import encode_password
from ..repositories import user
from ..middlewares.validation import validation
from ..schemas.user import UserSchema

def create_user():
    body = validation(UserSchema)
    
    username = body['username'] 
    email = body['email']
    password = body['password']
    
    db_user = user.find_by_username(username)
    db_email = user.find_by_email(email)
    if(db_user == {} or db_email == {}):
        raise Exception ("Conflict_error")

    hash = encode_password(password)

    user.insert(username, email, hash)

    return {"username": username}