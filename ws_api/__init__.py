from flask import Flask
from ws_api.routers.user_router import user_bp

def create_app():
    app = Flask(__name__)
    app.register_blueprint(user_bp)
    return app