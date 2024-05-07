import datetime as dt
from bson import ObjectId

from ..database import mongo

def find_all(user_id):
  return mongo.db.result.find({"user_id": ObjectId(user_id)})

def find_by_id(user_id, id):
  return mongo.db.result.aggregate([
    {
      "$match": {
        "_id": ObjectId(id), 
        "user_id": ObjectId(user_id)
      }
    },
    {
      "$lookup": {
        "from": "data",
        "localField": "data_id",
        "foreignField": "_id",
        "as": "data"
      }
    }
  ])

def insert(user_id, data):
  data["user_id"] = ObjectId(user_id)
  data["created_at"] = dt.datetime.now()
  return mongo.db.result.insert_one(data)

def update(user_id, id, name):
  return mongo.db.result.find_one_and_update({
    "_id": ObjectId(id), 
    'user_id': ObjectId(user_id)
  },
  {'$set': {"name": name, "updated_at": dt.datetime.now()}})

def delete(user_id, id):
  return mongo.db.result.find_one_and_delete({
    "_id": ObjectId(id), 
    'user_id': ObjectId(user_id)
  })