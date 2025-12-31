from flask import request, jsonify, redirect, url_for, session
from app.model.user import User
from werkzeug.security import check_password_hash, generate_password_hash
from app.response import success, error
from app.extensions import db


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
    data = request.json
    if not data:
        return error("Request harus JSON")

    user = User.query.filter_by(username=data.get('username')).first()
    if not user:
        return error("User tidak ditemukan", 404)

    if not check_password_hash(user.password, data.get('password')):
        return error("Password salah", 401)

    session['user_id'] = user.id_user
    session['role'] = user.role

    token = f"{user.id_user}:{user.role}"

    return success("Login berhasil", {
        "token": token,
        "role": user.role
    })


def register_api():
    data = request.json

    if not data:
        return jsonify({"message": "Request harus JSON"}), 400

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