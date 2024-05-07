import datetime as dt
from bson import ObjectId

from ..database import mongo

def find_by_id(id):
  return mongo.db.data.find_one({},{"_id": ObjectId(id)})

def find_by_user_id(id):
  return mongo.db.data.find({},{"user_id": ObjectId(id)})

def insert(user_id, info):
  return mongo.db.data.insert_one({
    "user_id": ObjectId(user_id),
    "info": info,
    "created_at": dt.datetime.now()
  })

def update(user_id, id, file):
  return mongo.db.data.find_one_and_update({
    "_id": ObjectId(id), 
    'user_id': ObjectId(user_id)
  },
  {'file': file})

def delete(user_id, id):
  return mongo.db.data.find_one_and_delete({
    "_id": ObjectId(id), 
    'user_id': ObjectId(user_id)
  })