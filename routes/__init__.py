from flask import Flask

def register_blueprint(app: Flask) -> None:
    from routes.core import core_bp

    app.register_blueprint(core_bp)