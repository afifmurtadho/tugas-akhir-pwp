from flask import request, session
from werkzeug.security import generate_password_hash, check_password_hash
from app.model.user import User
from app.extensions import db
from app.response import success, error

def get_users():
    users = User.query.all()
    data = [u.to_dict() for u in users]
    return success("List users", data)

def get_user(id):
    user = User.query.get(id)
    if not user:
        return error("User tidak ditemukan", 404)
    return success("Detail user", user.to_dict())

def create_user():
    data = request.json

    if not data:
        return error("Request harus JSON")

    username = data.get("username")
    password = data.get("password")
    nama_lengkap = data.get("nama_lengkap")
    role = data.get("role", "user")

    if not username or not password or not nama_lengkap:
        return error("Data tidak lengkap")

    user = User(
        username=username,
        password=generate_password_hash(password),
        nama_lengkap=nama_lengkap,
        role=role
    )

    db.session.add(user)
    db.session.commit()

    return success("User berhasil dibuat")


def update_user(id_user):
    user = User.query.get(id_user)
    if not user:
        return error("User tidak ditemukan", 404)

    data = request.json
    if not data:
        return error("Request harus JSON")

    user.username = data.get("username", user.username)
    user.nama_lengkap = data.get("nama_lengkap", user.nama_lengkap)
    user.role = data.get("role", user.role)

    db.session.commit()
    return success("User berhasil diupdate")


def delete_user(id):
    user = User.query.get(id)
    if not user:
        return error("User tidak ditemukan", 404)

    db.session.delete(user)
    db.session.commit()
    return success("User berhasil dihapus")


def login_user(request):
    username = request.form.get("username")
    password = request.form.get("password")

    user = User.query.filter_by(username=username).first()
    if not user:
        return error("User tidak ditemukan", 404)

    if not check_password_hash(user.password, password):
        return error("Password salah", 401)

    session["user_id"] = user.id
    session["role"] = user.role

    return success("Login berhasil")

def logout_user():
    session.clear()

