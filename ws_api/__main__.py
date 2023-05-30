from ws_api.__init__ import create_app
from ws_api.loadenv import config

app = create_app()

if __name__ == "__main__":
  app.run(host='127.0.0.1',debug=True, port=config["PORT"])