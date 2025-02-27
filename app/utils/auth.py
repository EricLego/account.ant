import jwt
import os
from flask import request, jsonify
from functools import wraps

SECRET_KEY = os.getenv("SECRET_KEY", "default_secret")

def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = request.headers.get("Authorization")

        if not token or not token.startswith("Bearer "):
            return jsonify({"error": "Token is missing"}), 401

        try:
            token = token.split(" ")[1]  # Extract token
            data = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
            request.user_id = data["sub"]
            request.user_role = data["role"]
        except jwt.ExpiredSignatureError:
            return jsonify({"error": "Token expired"}), 401
        except jwt.InvalidTokenError:
            return jsonify({"error": "Invalid token"}), 401

        return f(*args, **kwargs)
    
    return decorated
