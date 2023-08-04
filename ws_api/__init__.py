from flask import Flask
from flask_cors import CORS
from flask_compress import Compress
from .loadenv import config
from .database import mongo

from .controllers.health import health_bp
from .controllers.user import user_bp
from .controllers.session import session_bp
from .controllers.data import data_bp
from .controllers.mode import mode_bp
from .controllers.page import page_bp
from .controllers.result import result_bp

def create_app():
    app = Flask(__name__)
    CORS(app)

    app.config['SECRET_KEY'] = config['JWT_SECRET_KEY']
    app.config['MONGO_URI'] = config['MONGO_URI']
    mongo.init_app(app)

    # app.config["COMPRESS_REGISTER"] = False
    Compress().init_app(app)

    app.register_blueprint(health_bp)
    app.register_blueprint(user_bp)
    app.register_blueprint(session_bp)
    app.register_blueprint(data_bp)
    app.register_blueprint(mode_bp)
    app.register_blueprint(page_bp)
    app.register_blueprint(result_bp)

    return app