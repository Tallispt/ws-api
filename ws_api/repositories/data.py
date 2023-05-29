import datetime as dt
from bson.json_util import dumps

from ..database import mongo

def find():
  result = mongo.db.data.find()
  list_cur = list(result)
  data = dumps(list_cur)
  return data

def insert(name, file):
  return mongo.db.data.insert_one({
    "name": name,
    "file": file,
    "created_at": dt.datetime.now()
  })