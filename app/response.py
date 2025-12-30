from flask import jsonify

def success(message, data=None, code=200):
    return jsonify({
        "status": "success",
        "message": message,
        "data": data
    }), code

def error(message, code=400):
    return jsonify({
        "status": "error",
        "message": message
    }), code
