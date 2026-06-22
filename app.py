from flask import Flask

def create_app(config=None):
    app = Flask(__name__)

    from routes import register_blueprint
    register_blueprint(app)

    return app

if __name__ == "__main__":
    create_app().run()