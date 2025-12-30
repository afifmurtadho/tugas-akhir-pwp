from app.model.user import User
from app.extensions import db
from flask import session
from app.response import success, error
from werkzeug.security import generate_password_hash, check_password_hash


def get_users():
    return User.query.all()


def get_user(id):
    user = User.query.get(id)
    if not user:
        return error("User tidak ditemukan", 404)
    return success("Detail user", user.to_dict())

def create_user(request):
    username = request.form.get("username")
    password = request.form.get("password")
    role = request.form.get("role", "user")

    if not username or not password:
        return error("Data tidak lengkap")

    user = User(
        username=username,
        password=generate_password_hash(password),
        role=role
    )
    db.session.add(user)
    db.session.commit()

    return success("User berhasil dibuat")


def update_user(request, id):
    user = User.query.get(id)
    if not user:
        return error("User tidak ditemukan", 404)

    user.username = request.form.get("username", user.username)
    user.role = request.form.get("role", user.role)

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

