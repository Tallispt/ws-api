from flask import Flask

from ..database import mongo
from ..loadenv import config
from .page_seed import seed_page


def connect_mongo():
    app = Flask(__name__)
    app.config["MONGO_URI"] = config["MONGO_URI"]
    mongo.init_app(app)


def seed_all():
    try:
        connect_mongo()
        seed_page()
    except Exception as e:
        print(e)
