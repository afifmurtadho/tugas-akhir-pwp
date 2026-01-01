from flask import Flask, request
from config import Config
from app.extensions import db, migrate, jwt
from app.routes.routes_web import web
from app.routes.routes_api import api

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)
    migrate.init_app(app, db)

    # JWT
    app.config['JWT_SECRET_KEY'] = app.config.get('SECRET_KEY')
    jwt.init_app(app)

    app.register_blueprint(web)
    app.register_blueprint(api)

    # Configure logging so Werkzeug request logs are emitted to the terminal
    import logging
    from logging import StreamHandler, Formatter

    handler = StreamHandler()
    handler.setLevel(logging.DEBUG)
    handler.setFormatter(Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s'))

    app.logger.setLevel(logging.DEBUG)
    app.logger.addHandler(handler)

    werkzeug_logger = logging.getLogger('werkzeug')
    werkzeug_logger.setLevel(logging.DEBUG)
    werkzeug_logger.addHandler(handler)

    @app.before_request
    def log_request_info():
        app.logger.debug(f"Request: {request.method} {request.path} from {request.remote_addr}")

    return app
