from ws_api import mongo

users = mongo.db.users

def find_by_username(username):
    return users.find_one({"username": username})

def find_by_email(email):
    return users.find_one({"email": email})

def insert(username, email, hash):
    return users.insert_one({"username": username, "email": email, "password": hash })
