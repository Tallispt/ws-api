from ws_api.__init__ import create_app

def main():
    app = create_app()
    return app

def test():
    app = create_app()
    app.run(host='127.0.0.1',debug=True, port=5000)

if __name__ == "__main__":
    main()