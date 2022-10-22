from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import os

basedir = os.path.abspath(os.path.dirname(__file__))

db = SQLAlchemy()


def create_app():
    app = Flask(__name__)
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///" + os.path.join(
        basedir, "../database/db.db"
    )
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    from src import models

    db.init_app(app)

    from src.routes import api

    app.register_blueprint(api)

    return app
