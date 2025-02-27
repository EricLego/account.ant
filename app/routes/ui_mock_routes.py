# app/routes/ui_mock_routes.py
import re
import bcrypt
import datetime
from flask import Blueprint, request, jsonify, current_app

ui_mock_bp = Blueprint("ui_mock", __name__)

# In-memory stores for this mock prototype:
MOCK_USERS = {}       # Approved/active users keyed by email
PENDING_USERS = {}    # New user requests awaiting admin approval
USER_COUNTER = 1      # Simple counter for user IDs

# --- Utility Functions ---

def validate_password(password, previous_passwords=[]):
    """Enforce password policy:
       - Minimum 8 characters
       - Starts with a letter
       - Contains at least one letter, one number, and one special character.
       - Cannot match any previously used password.
    """
    if len(password) < 8:
        return False, "Password must be at least 8 characters long."
    if not password[0].isalpha():
        return False, "Password must start with a letter."
    if not re.search(r"[A-Za-z]", password):
        return False, "Password must contain a letter."
    if not re.search(r"\d", password):
        return False, "Password must contain a number."
    if not re.search(r"[!@#$%^&*(),.?\":{}|<>]", password):
        return False, "Password must contain a special character."
    # For this mock, we assume previous_passwords contains plaintext values for checking
    if password in previous_passwords:
        return False, "New password must not be one used previously."
    return True, ""

def generate_username(first_name, last_name, creation_date):
    """Generate username as: first name initial + full last name + MMYY (account creation date)."""
    return first_name[0].lower() + last_name.lower() + creation_date.strftime("%m%y")

# --- Endpoint Implementations ---

@ui_mock_bp.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    if "email" not in data or "password" not in data:
        return jsonify({"error": "Email and password are required."}), 400
    email = data["email"]
    password = data["password"]
    user = MOCK_USERS.get(email)
    if not user:
        return jsonify({"error": "User not found."}), 404
    # Check if user is suspended
    if not user["active"]:
        return jsonify({"error": "User is suspended."}), 403
    # Validate password
    if not bcrypt.checkpw(password.encode("utf-8"), user["password_hash"].encode("utf-8")):
        user["wrong_attempts"] += 1
        if user["wrong_attempts"] >= 3:
            user["active"] = False
            return jsonify({"error": "Account suspended due to multiple wrong attempts."}), 403
        return jsonify({"error": "Invalid credentials."}), 401
    # Reset wrong attempt counter on successful login
    user["wrong_attempts"] = 0
    # Return login info including username, picture, and role
    return jsonify({
        "message": "Login successful.",
        "user": {
            "username": user["username"],
            "picture": user.get("picture", "default.png"),
            "role": user["role"]
        }
    }), 200

@ui_mock_bp.route('/signup', methods=['POST'])
def signup():
    data = request.get_json()
    required_fields = ["first_name", "last_name", "email", "password", "address", "dob"]
    for field in required_fields:
        if field not in data:
            return jsonify({"error": f"Missing field: {field}"}), 400
    email = data["email"]
    if email in MOCK_USERS or email in PENDING_USERS:
        return jsonify({"error": "User already exists or request is pending."}), 400
    valid, msg = validate_password(data["password"])
    if not valid:
        return jsonify({"error": msg}), 400
    global USER_COUNTER
    creation_date = datetime.datetime.now()
    username = generate_username(data["first_name"], data["last_name"], creation_date)
    pending_user = {
        "user_id": USER_COUNTER,
        "first_name": data["first_name"],
        "last_name": data["last_name"],
        "email": email,
        "address": data["address"],
        "dob": data["dob"],
        "password_hash": bcrypt.hashpw(data["password"].encode("utf-8"), bcrypt.gensalt()).decode("utf-8"),
        "role": "regular",   # default to regular user; admin may update this later
        "active": False,     # not active until approved by an administrator
        "username": username,
        "wrong_attempts": 0,
        "previous_passwords": [],
        "created_at": creation_date.isoformat(),
        "picture": data.get("picture", "default.png")
    }
    PENDING_USERS[email] = pending_user
    USER_COUNTER += 1
    # Simulate sending an email to the administrator for approval
    print(f"[MOCK] New user request for {email} pending admin approval.")
    return jsonify({"message": "User request submitted. Await admin approval."}), 201

@ui_mock_bp.route('/admin/approve_user', methods=['POST'])
def approve_user():
    data = request.get_json()
    if "email" not in data:
        return jsonify({"error": "Email is required."}), 400
    email = data["email"]
    pending_user = PENDING_USERS.pop(email, None)
    if not pending_user:
        return jsonify({"error": "No pending user request for this email."}), 404
    # Optionally allow admin to assign a role during approval
    role = data.get("role", "regular")
    pending_user["role"] = role
    pending_user["active"] = True
    MOCK_USERS[email] = pending_user
    print(f"[MOCK] Admin approved user {email}. Approval email sent to user.")
    return jsonify({"message": f"User {email} approved and activated."}), 200

@ui_mock_bp.route('/admin/update_user', methods=['POST'])
def update_user():
    data = request.get_json()
    if "email" not in data:
        return jsonify({"error": "Email is required."}), 400
    email = data["email"]
    user = MOCK_USERS.get(email)
    if not user:
        return jsonify({"error": "User not found."}), 404
    # Update allowed fields: first name, last name, address, role
    for field in ["first_name", "last_name", "address", "role"]:
        if field in data:
            user[field] = data[field]
    return jsonify({"message": f"User {email} updated successfully."}), 200

@ui_mock_bp.route('/admin/suspend_user', methods=['POST'])
def suspend_user():
    data = request.get_json()
    if "email" not in data or "start_date" not in data or "end_date" not in data:
        return jsonify({"error": "Email, start_date, and end_date are required."}), 400
    email = data["email"]
    user = MOCK_USERS.get(email)
    if not user:
        return jsonify({"error": "User not found."}), 404
    user["suspended_from"] = data["start_date"]
    user["suspended_until"] = data["end_date"]
    us
