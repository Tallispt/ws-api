from ..database import mongo

# users = mongo.db.users

def find_by_username(username):
    return mongo.db.users.find_one({"username": username})
    return

def find_by_email(email):
    return mongo.db.users.find_one({"email": email})

def insert(username, email, hash):
    return mongo.db.users.insert_one({"username": username, "email": email, "password": hash })
