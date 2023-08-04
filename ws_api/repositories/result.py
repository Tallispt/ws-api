from ..database import mongo

def find_all():
  return mongo.db.result.find()