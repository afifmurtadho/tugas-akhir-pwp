from flask import Blueprint, request, jsonify
from app.controller.AuthController import login_api, logout_api
from app.controller.UserController import (
    create_user, get_users, update_user, delete_user
)
from app.middleware.auth import login_required, admin_required

api = Blueprint('api', __name__, url_prefix='/api')

# ---------- AUTH ----------
@api.route('/login', methods=['POST'])
def login():
    return login_api()

@api.route('/logout', methods=['POST'])
@login_required
def logout():
    return logout_api()

# ---------- USERS ----------
@api.route('/users', methods=['GET'])
@login_required
@admin_required
def users():
    return get_users()

@api.route('/users', methods=['POST'])
@login_required
@admin_required
def add_user():
    return create_user(request)

@api.route('/users/<int:id_user>', methods=['PUT'])
@login_required
@admin_required
def edit_user(id_user):
    return update_user(request, id_user)

@api.route('/users/<int:id_user>', methods=['DELETE'])
@login_required
@admin_required
def remove_user(id_user):
    return delete_user(id_user)
