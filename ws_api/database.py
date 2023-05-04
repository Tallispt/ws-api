from pymongo import MongoClient
from ws_api.utils.loadenv import config

client = MongoClient(config['MONGO_URI'])
mongo = client[config['MONGO_DB_NAME']]