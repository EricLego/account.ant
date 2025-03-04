from flask import Blueprint, request, jsonify
#from flask import current_app
from functools import wraps
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
    # from flask import current_app
    """Authenticate user and return JWT token."""
    # EXPIRY_HOURS = current_app.config.get("JWT_EXPIRY_HOURS", 1)

    data = request.get_json()
    email = data.get('email')
    password = data.get('password')

    if not email or not password:
        return jsonify({"error": "Email and password are required"}), 400

    # Query user using SQLAlchemy ORM
    user = User.query.filter_by(email=email).first()

    if not user or not user.verify_password(user, password):
        return jsonify({"error": "Invalid email or password"}), 401

    if not user.status:
        return jsonify({"error": "Account is suspended"}), 403

    # Generate JWT token
    token = jwt.encode({
        "sub": f"{user.user_id}",  # Store user_id as string
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

def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = request.headers.get("Authorization")

        if not token:
            return jsonify({"error": "Token is missing"}), 401

        try:
            decoded = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
            request.user_id = decoded["sub"]
            request.user_role = decoded["role"]
        except jwt.ExpiredSignatureError:
            return jsonify({"error": "Token expired"}), 401
        except jwt.InvalidTokenError:
            return jsonify({"error": "Invalid token"}), 401

        return f(*args, **kwargs)
    return decorated