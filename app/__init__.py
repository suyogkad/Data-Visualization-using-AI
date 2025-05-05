# app/__init__.py
from flask import Flask
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

def create_app():
    app = Flask(__name__,
                template_folder="templates",
                static_folder="static")
    app.config.from_object("config.Config")
    db.init_app(app)

    from .routes import bp as main_bp
    app.register_blueprint(main_bp)

    return app
