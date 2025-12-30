from flask import Flask
from config import Config
from app.extensions import db, migrate
from app.routes.routes_web import web
from app.routes.routes_api import api

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)
    migrate.init_app(app, db)

    app.register_blueprint(web)
    app.register_blueprint(api)

    return app
