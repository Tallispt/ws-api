import datetime as dt

from ..database import mongo
from ..schemas.user import UserSchema

def find_by_username(username):
    user = mongo.db.users.find_one({"username": username})
    return UserSchema().dumps(user)

def find_by_email(email):
    user = mongo.db.users.find_one({"email": email})
    return UserSchema().dumps(user)

def insert(username, email, hash):
    return mongo.db.users.insert_one({
        "username": username, 
        "email": email, 
        "password": hash, 
         "created_at": dt.datetime.now() })
