from flask import Flask
from flask_compress import Compress
from flask_cors import CORS

from .bucket import firebase
from .controllers.data import data_bp
from .controllers.health import health_bp
from .controllers.result import result_bp
from .controllers.session import session_bp
from .controllers.user import user_bp
from .database import mongo
from .loadenv import config


def create_app():
    app = Flask(__name__)
    CORS(app)

    app.config["SECRET_KEY"] = config["JWT_SECRET_KEY"]
    app.config["MONGO_URI"] = config["MONGO_URI"]
    app.config["CRED_PATH"] = config["CRED_PATH"]
    app.config["BUCKET_URI"] = config["BUCKET_URI"]
    mongo.init_app(app)
    firebase.init_app(app)

    # app.config["COMPRESS_REGISTER"] = False
    Compress().init_app(app)

    app.register_blueprint(health_bp)
    app.register_blueprint(user_bp)
    app.register_blueprint(session_bp)

    app.register_blueprint(data_bp)
    app.register_blueprint(result_bp)

    return app
