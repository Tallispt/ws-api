from ws_api.database.db import mongo
from bson import ObjectId

sessions = mongo.db.sessions

def find_by_session_id(sessionId):
  # user = users.find_one({"username": username})
  # return decode_utils.parse_json(user)
  return

def insert(data):
  return sessions.insert_one(data)
