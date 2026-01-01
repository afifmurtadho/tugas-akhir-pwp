from flask import request, jsonify, redirect, url_for, session
from app.model.user import User
from werkzeug.security import check_password_hash, generate_password_hash
from app.response import success, error
from app.extensions import db
from flask_jwt_extended import create_access_token, create_refresh_token, jwt_required, get_jwt_identity



def login_web():
    username = request.form.get('username')
    password = request.form.get('password')

    user = User.query.filter_by(username=username).first()

    if not user:
        return redirect(url_for('web.login'))

    if not check_password_hash(user.password, password):
        return redirect(url_for('web.login'))

    session['user_id'] = user.id_user
    session['role'] = user.role

    return redirect(url_for('web.dashboard'))


def login_api():
    # accept either JSON or form-encoded body
    data = request.get_json(silent=True) or request.form
    if not data:
        return error("Request harus berisi data username/password")

    user = User.query.filter_by(username=data.get('username')).first()
    if not user:
        return error("User tidak ditemukan", 404)

    if not check_password_hash(user.password, data.get('password')):
        return error("Password salah", 401)
    # keep session for existing session-based middleware compatibility
    session['user_id'] = user.id_user
    session['role'] = user.role

    access_token = create_access_token(identity=str(user.id_user), additional_claims={"role": user.role})
    refresh_token = create_refresh_token(identity=str(user.id_user))

    return success("Login berhasil", {
        "access_token": access_token,
        "refresh_token": refresh_token,
        "role": user.role
    })


def register_api():
    data = request.get_json(silent=True) or request.form

    if not data:
        return jsonify({"message": "Request harus berisi data"}), 400

    username = data.get("username")
    password = data.get("password")
    nama_lengkap = data.get("nama_lengkap")
    role = data.get("role", "user")

    if not username or not password or not nama_lengkap:
        return jsonify({"message": "Data tidak lengkap"}), 400

    if User.query.filter_by(username=username).first():
        return jsonify({"message": "Username sudah terdaftar"}), 409

    user = User(
        username=username,
        password=generate_password_hash(password),
        nama_lengkap=nama_lengkap,
        role=role
    )

    db.session.add(user)
    db.session.commit()

    return jsonify({
        "message": "Register berhasil",
        "username": username,
        "role": role
    }), 201


def logout_api():
    session.clear()
    return success("Logout berhasil")


def refresh_api():
    # expects a valid refresh token via Authorization: Bearer <refresh_token>
    identity = get_jwt_identity()
    if not identity:
        return error("Refresh token invalid", 401)

    new_access = create_access_token(identity=identity)
    return success("Token refreshed", {"access_token": new_access})