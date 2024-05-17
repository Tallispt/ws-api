from ws_api.__init__ import create_app
from ws_api.loadenv import config

def main():
    from waitress import serve
    app = create_app()
    serve(app, host="0.0.0.0", port=8080)

def test():
    app = create_app()
    app.run(host='127.0.0.1',debug=True, port=5000)

if __name__ == "__main__":
    main()