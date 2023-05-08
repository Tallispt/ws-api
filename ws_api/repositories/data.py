from..database import mongo

def find():
  return mongo.db.data.find()

def insert(data):
  return mongo.db.data.insert_one(data)