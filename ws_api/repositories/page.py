import datetime as dt

from ..database import mongo

def find_all():
    return mongo.db.pages.find()

def insert(name, icon, route):
    return mongo.db.pages.insert_one({
        "name": name, 
        "icon": icon, 
        "route": route, 
        "created_at": dt.datetime.now() })

