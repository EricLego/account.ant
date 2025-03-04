import jwt
import os
from flask import request, jsonify
from flask import current_app
from functools import wraps

SECRET_KEY = os.getenv("SECRET_KEY", "default_secret")

def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        auth_header = request.headers.get("Authorization")
        if not auth_header or not auth_header.startswith("Bearer "):
            return jsonify({"error": "Token is missing"}), 401

        parts = auth_header.split(" ")
        if len(parts) != 2:
            return jsonify({"error": "Invalid token format"}), 401

        token = parts[1]

        try:
            data = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
            # Store user data in the request context for downstream use.
            request.user_id = data.get("sub")
            request.user_role = data.get("role")
        except jwt.ExpiredSignatureError as e:
            # Optional: log the error for debugging
            current_app.logger.warning(f"Token expired: {str(e)}")
            return jsonify({"error": "Token expired"}), 401
        except jwt.InvalidTokenError as e:
            # Optional: log the error for debugging
            current_app.logger.warning(f"Invalid token: {str(e)}")
            return jsonify({"error": "Invalid token"}), 401

        return f(*args, **kwargs)
    
    return decorated
