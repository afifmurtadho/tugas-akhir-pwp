from functools import wraps
from flask import session, redirect, url_for, jsonify

def login_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        if 'user_id' not in session:
            return redirect(url_for('web.login'))
        return f(*args, **kwargs)
    return decorated

def admin_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        if session.get('role') != 'admin':
            return jsonify({'message': 'Admin only'}), 403
        return f(*args, **kwargs)
    return decorated
