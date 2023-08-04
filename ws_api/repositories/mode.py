import datetime as dt
from bson import ObjectId

from ..database import mongo

def find_all(user_id):
  return mongo.db.mode.find({"user_id": ObjectId(user_id)})

def find_by_id(id, user_id):
  return mongo.db.mode.find_one({"_id": ObjectId(id), "user_id": ObjectId(user_id)})

def find_by_title(title, user_id):
  return mongo.db.mode.find_one({"title": title, "user_id": ObjectId(user_id)})

def find_by_type(type, user_id):
  return mongo.db.mode.find({"type": type, "user_id": ObjectId(user_id)})

def insert(data, user_id):
  data["user_id"] = ObjectId(user_id)
  data["created_at"] = dt.datetime.now()
  return mongo.db.mode.insert_one(data)

def update(id, user_id, info):
  info["updated_at"] = dt.datetime.now()
  return mongo.db.mode.find_one_and_update({
    "_id": ObjectId(id), 
    'user_id': ObjectId(user_id)
  },
  {'$set': info})

def delete(id, user_id):
  return mongo.db.mode.find_one_and_delete({
    "_id": ObjectId(id), 
    'user_id': ObjectId(user_id)
  })