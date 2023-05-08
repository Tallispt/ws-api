from flask import Flask
from flask_cors import CORS
from .loadenv import config
from .database import mongo

from .controllers.health import health_bp
from .controllers.user import user_bp
from .controllers.session import session_bp
from .controllers.data import data_bp

def create_app():
    app = Flask(__name__)
    CORS(app)

    app.config['MONGO_URI'] = config['MONGO_URI']
    mongo.init_app(app)

    app.register_blueprint(health_bp)
    app.register_blueprint(user_bp)
    app.register_blueprint(session_bp)
    app.register_blueprint(data_bp)

    return app