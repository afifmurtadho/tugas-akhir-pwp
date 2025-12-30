from flask import request, jsonify, redirect, url_for, session
from app.model.user import User
from werkzeug.security import check_password_hash
from app import db

def login():
    data = request.get_json()

    if not data:
        return jsonify({'message': 'Request harus JSON'}), 400

    user = User.query.filter_by(username=data.get('username')).first()

    if not user:
        return jsonify({'message': 'User tidak ditemukan'}), 404

    if not check_password_hash(user.password, data.get('password')):
        return jsonify({'message': 'Password salah'}), 401

    return jsonify({
        'message': 'Login berhasil',
        'id_user': user.id_user,
        'username': user.username,
        'role': user.role
    }), 200

# =========================
# LOGIN UNTUK WEB (HTML)
# =========================
def login_web():
    username = request.form.get('username')
    password = request.form.get('password')

    user = User.query.filter_by(username=username).first()

    if not user:
        return redirect(url_for('web.login'))

    if not check_password_hash(user.password, password):
        return redirect(url_for('web.login'))

    # simpan session
    session['user_id'] = user.id_user
    session['role'] = user.role

    return redirect(url_for('web.dashboard'))


def login_api(request):
    data = request.json

    user = User.query.filter_by(username=data.get('username')).first()
    if not user:
        return jsonify({'message': 'User not found'}), 404

    if not check_password_hash(user.password, data.get('password')):
        return jsonify({'message': 'Wrong password'}), 401

    session['user_id'] = user.id_user
    session['role'] = user.role

    return jsonify({
        'message': 'Login success',
        'role': user.role
    })


def logout_api():
    session.clear()
    return jsonify({'message': 'Logout success'})
