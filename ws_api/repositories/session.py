from bson import ObjectId

from..database import mongo
from ..utils.decode import parse_json

def find_by_session_id(session_id):
  user = mongo.db.sessions.find_one({"_id": ObjectId(session_id)})
  return parse_json(user)

def insert(data):
  return mongo.db.sessions.insert_one(data)

def delete_by_session_id(session_id):
  mongo.db.session.find_one_and_delete({"_id": ObjectId(session_id)})