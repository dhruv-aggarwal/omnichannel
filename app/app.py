from db import db
from routes import load_blueprints
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate, MigrateCommand
from wsgi_middleware import HTTPMethodOverrideMiddleware


def create_app():
    app = Flask(__name__, instance_relative_config=True)
    app.wsgi_app = HTTPMethodOverrideMiddleware(app.wsgi_app)
    app.config.from_object('settings')

    db.init_app(app)
    app = load_blueprints(app)

    return app
