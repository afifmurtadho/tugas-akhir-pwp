from flask import Blueprint

web = Blueprint('web', __name__)
api = Blueprint('api', __name__)

from app.routes import routes_web, routes_api
