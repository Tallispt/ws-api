from ws_api import create_app
from flask_cors import CORS
from ws_api.database.db import mongodb_config
from ws_api.utils.loadenv import config

app = create_app()
CORS(app)
mongo = mongodb_config(app, config)

if __name__ == "__main__":
  app.run(host='127.0.0.1', debug=True, port=config["PORT"])