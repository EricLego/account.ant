# app/routes/test_routes.py
import re
import bcrypt
from flask import Blueprint, request, jsonify, current_app

# Create a blueprint for our test routes
test_bp = Blueprint("test", __name__)

# Global in-memory store for mock users (keyed by email)
MOCK_USERS = {}

def is_valid_email(email: str) -> bool:
    """Simple email validation using regex."""
    pattern = r"^[\w\.-]+@[\w\.-]+\.\w+$"
    return re.match(pattern, email) is not None

# Mock helper functions
def mock_add_user(data):
    email = data["email"]
    if email in MOCK_USERS:
        return None, "Email already registered"
    user_id = len(MOCK_USERS) + 1
    # Store user data in a dictionary (simulate a DB row)
    new_user = {
        "user_id": user_id,
        "first_name": data["first_name"],
        "last_name": data["last_name"],
        "email": email,
        "password_hash": bcrypt.hashpw(data["password"].encode("utf-8"), bcrypt.gensalt()).decode("utf-8"),
        "role": 1,
        "status": True,
    }
    MOCK_USERS[email] = new_user
    return new_user, None

def mock_get_user(email):
    return MOCK_USERS.get(email)

@test_bp.route('/signup', methods=['POST'])
def signup():
    data = request.get_json()
    # Check for required fields
    for field in ["first_name", "last_name", "email", "password"]:
        if field not in data:
            return jsonify({"error": f"Missing field: {field}"}), 400

    email = data["email"]
    if not is_valid_email(email):
        return jsonify({"error": "Invalid email address"}), 400

    # Check if we are in mock mode
    if current_app.config.get("MOCK_MODE", False):
        if mock_get_user(email):
            return jsonify({"error": "Email already registered"}), 400
        new_user, err = mock_add_user(data)
        if err:
            return jsonify({"error": err}), 400
        # Simulate sending a validation email
        print(f"[MOCK] Validation email sent to {email}")
        return jsonify({
            "message": "User created successfully in mock mode. A validation email has been sent.",
            "user_id": new_user["user_id"]
        }), 201
    else:
        # Real mode (using SQLAlchemy) – make sure your models are working properly if you switch this off
        from app.models import db
        from app.models.user import User
        if User.query.filter_by(email=email).first():
            return jsonify({"error": "Email already registered"}), 400
        new_user = User(
            first_name=data["first_name"],
            last_name=data["last_name"],
            email=email,
            password_hash=User.hash_password(data["password"]),
            role=1,
            status=True
        )
        db.session.add(new_user)
        db.session.commit()
        print(f"Validation email sent to {email}")
        return jsonify({
            "message": "User created successfully.",
            "user_id": new_user.user_id
        }), 201

@test_bp.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    if "email" not in data or "password" not in data:
        return jsonify({"error": "Email and password are required"}), 400

    email = data["email"]
    password = data["password"]

    if current_app.config.get("MOCK_MODE", False):
        user = mock_get_user(email)
        if not user or not bcrypt.checkpw(password.encode("utf-8"), user["password_hash"].encode("utf-8")):
            return jsonify({"error": "Invalid email or password"}), 401
        return jsonify({
            "message": "Login successful in mock mode",
            "user_id": user["user_id"]
        }), 200
    else:
        from app.models.user import User
        user = User.query.filter_by(email=email).first()
        if not user or not user.verify_password(password):
            return jsonify({"error": "Invalid email or password"}), 401
        return jsonify({
            "message": "Login successful",
            "user_id": user.user_id
        }), 200

@test_bp.route('/send_validation', methods=['POST'])
def send_validation():
    data = request.get_json()
    if "email" not in data:
        return jsonify({"error": "Email is required"}), 400

    email = data["email"]
    if not is_valid_email(email):
        return jsonify({"error": "Invalid email address"}), 400

    # Simulate sending a validation email
    print(f"[MOCK] Validation email sent to {email}")
    return jsonify({"message": f"Validation email sent to {email}"}), 200
