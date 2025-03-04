from flask import Blueprint, request, jsonify
from app.models import db
from app.models.user import User
import jwt
from jwt.exceptions import ExpiredSignatureError, InvalidTokenError
import datetime
import os

auth_bp = Blueprint('auth', __name__)

# Load SECRET_KEY from environment variables
SECRET_KEY = os.getenv("SECRET_KEY", "your_secret_key")

@auth_bp.route('/auth/login', methods=['POST'])
def login():
    """Authenticate user and return JWT token."""
    data = request.get_json()
    email = data.get('email')
    password = data.get('password')

    if not email or not password:
        return jsonify({"error": "Email and password are required"}), 400

    # Query user using SQLAlchemy ORM
    user = User.query.filter_by(email=email).first()

    if not user or not user.verify_password(password):
        return jsonify({"error": "Invalid email or password"}), 401

    if not user.status:
        return jsonify({"error": "Account is suspended"}), 403

    # Generate JWT token
    token = jwt.encode({
        "sub": user.user_id,  # Store user_id instead of email
        "name": f"{user.first_name} {user.last_name}",
        "role": user.role,
        "exp": datetime.datetime.utcnow() + datetime.timedelta(hours=1)
    }, SECRET_KEY, algorithm="HS256")

    return jsonify({
        "token": token,
        "role": user.role,
        "name": f"{user.first_name} {user.last_name}"
    }), 200


@auth_bp.route('/auth/validate', methods=['POST'])
def validate_token():
    """Validate JWT token and return user details."""
    data = request.get_json()
    token = data.get("token")

    if not token:
        return jsonify({"error": "Token is required"}), 400

    try:
        decoded = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
        return jsonify({
            "valid": True,
            "user_id": decoded["sub"],
            "name": decoded["name"],
            "role": decoded["role"]
        }), 200
    except ExpiredSignatureError:
        return jsonify({"valid": False, "error": "Token expired"}), 401
    except InvalidTokenError:
        return jsonify({"valid": False, "error": "Invalid token"}), 401
