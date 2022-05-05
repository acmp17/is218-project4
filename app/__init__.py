"""A flask web app"""
import os

import flask_login
from flask import Flask
from flask_bootstrap import Bootstrap5
from flask_wtf.csrf import CSRFProtect

from app.auth import auth
from app.cli import create_database, create_log_folder
from app.context_processors import utility_text_processors
from app.db import db
from app.db import database
from app.db.models import User

login_manager = flask_login.LoginManager()

def create_app():
    """Create and configure an instance of the Flask application."""
    app = Flask(__name__)
    app.secret_key = 'This is an INSECURE secret!! DO NOT use this in production!!'
    if os.environ.get("FLASK_ENV") == "production":
        app.config.from_object("app.config.ProductionConfig")
    elif os.environ.get("FLASK_ENV") == "development":
        app.config.from_object("app.config.DevelopmentConfig")
    elif os.environ.get("FLASK_ENV") == "testing":
        app.config.from_object("app.config.TestingConfig")

    login_manager.init_app(app)
    login_manager.login_view = "auth.login"
    csrf = CSRFProtect(app)
    bootstrap = Bootstrap5(app)

    db_dir = "database/db.sqlite"
    app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///" + os.path.abspath(db_dir)
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    db.init_app(app)
    # add command function to cli commands
    app.cli.add_command(create_database)

    @app.route('/')
    def hello():
        return 'Hello, World!'

    return app

@login_manager.user_loader
def user_loader(user_id):
    try:
        return User.query.get(int(user_id))
    except:
        return None