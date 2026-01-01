from functools import wraps
from flask import jsonify
from flask_jwt_extended import verify_jwt_in_request, get_jwt


def login_required(f):
    @wraps(f)
    def wrapper(*args, **kwargs):
        try:
            verify_jwt_in_request()
        except Exception as e:
            return jsonify({"message": "Unauthorized", "error": str(e)}), 401
        return f(*args, **kwargs)

    return wrapper


def admin_required(f):
    @wraps(f)
    def wrapper(*args, **kwargs):
        try:
            verify_jwt_in_request()
        except Exception as e:
            return jsonify({"message": "Unauthorized", "error": str(e)}), 401

        claims = get_jwt()
        if claims.get("role") != "admin":
            return jsonify({"message": "Admin only"}), 403
        return f(*args, **kwargs)

    return wrapper

