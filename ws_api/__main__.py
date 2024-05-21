from ws_api.__init__ import create_app

app = create_app()


def test():
    app.run(host="127.0.0.1", debug=True, port=5000)
