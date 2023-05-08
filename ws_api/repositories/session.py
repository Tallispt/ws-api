import datetime as dt
from bson import ObjectId

from..database import mongo
from ..schemas.session import SessionSchema

def find_by_session_id(session_id):
  session = mongo.db.sessions.find_one({"_id": ObjectId(session_id)})
  return SessionSchema().dumps(session)

def find_by_token(token):
  session = mongo.db.sessions.find_one({'token': token})
  return SessionSchema().dumps(session)

def insert(user_id, uuid_obj):
  return mongo.db.sessions.insert_one({
    "user_id": user_id,
    "token": uuid_obj,
    "is_valid": True,
    "created_at": dt.datetime.now()
  })

def delete_by_session_id(session_id):
  mongo.db.sessions.find_one_and_delete({"_id": ObjectId(session_id)})

def delete_all():
  mongo.db.sessions.delete_many({})