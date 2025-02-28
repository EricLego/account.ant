# app/routes/ui_mock_routes.py
import re
import bcrypt
import datetime
import uuid
from flask import Blueprint, request, jsonify

ui_mock_bp = Blueprint("ui_mock", __name__)

# In-memory mock stores
MOCK_USERS = {}         # Approved/active users keyed by email
PENDING_USERS = {}      # New user requests awaiting admin approval
USER_TOKENS = {}        # token -> email
USER_COUNTER = 1        # Simple counter for user IDs

# --- Utility Functions ---

def validate_password(password, previous_passwords=[]):
    """
    Enforce password policy:
    - Minimum 8 characters
    - Starts with a letter
    - Contains at least one letter, one number, and one special character
    - Must not match any previously used password
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
    if password in previous_passwords:
        return False, "New password must not be one used previously."
    return True, ""

def generate_username(first_name, last_name, creation_date):
    """
    Generate username as: first name initial + full last name + MMYY
    Example: John Doe created 02/25 => jdoe0225
    """
    return first_name[0].lower() + last_name.lower() + creation_date.strftime("%m%y")

# --- AUTH ENDPOINTS ---

@ui_mock_bp.route('/auth/login', methods=['POST'])
def login():
    data = request.get_json()
    if "email" not in data or "password" not in data:
        return jsonify({"error": "Email and password are required."}), 400

    email = data["email"]
    password = data["password"]
    user = MOCK_USERS.get(email)
    if not user:
        return jsonify({"error": "User not found."}), 404

    if not user["active"]:
        return jsonify({"error": "User is suspended."}), 403

    # Check password
    if not bcrypt.checkpw(password.encode("utf-8"), user["password_hash"].encode("utf-8")):
        user["wrong_attempts"] += 1
        if user["wrong_attempts"] >= 3:
            user["active"] = False
            return jsonify({"error": "Account suspended after multiple wrong attempts."}), 403
        return jsonify({"error": "Invalid credentials."}), 401

    # Reset wrong attempts on success
    user["wrong_attempts"] = 0

    # Generate a mock token and store it
    token = str(uuid.uuid4())
    USER_TOKENS[token] = email

    return jsonify({
        "message": "Login successful.",
        "token": token,
        "role": user["role"]
    }), 200

@ui_mock_bp.route('/auth/validate', methods=['POST'])
def validate_token():
    data = request.get_json()
    token = data.get("token")
    if not token or token not in USER_TOKENS:
        return jsonify({"error": "Invalid token"}), 401

    email = USER_TOKENS[token]
    user = MOCK_USERS.get(email)
    if not user:
        return jsonify({"error": "User not found for token"}), 401

    return jsonify({
        "message": "Token is valid.",
        "name": user["first_name"] + " " + user["last_name"]
    }), 200

@ui_mock_bp.route('/auth/signup-request', methods=['POST'])
def signup_request():
    data = request.get_json()
    required_fields = ["firstName", "lastName", "email", "password", "address", "dob"]
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
    username = generate_username(data["firstName"], data["lastName"], creation_date)

    pending_user = {
        "user_id": USER_COUNTER,
        "first_name": data["firstName"],
        "last_name": data["lastName"],
        "email": email,
        "address": data["address"],
        "dob": data["dob"],
        "password_hash": bcrypt.hashpw(data["password"].encode("utf-8"), bcrypt.gensalt()).decode("utf-8"),
        "role": "regular",      # default role
        "active": False,        # becomes true once approved
        "username": username,
        "wrong_attempts": 0,
        "previous_passwords": [],
        "created_at": creation_date.isoformat(),
        "picture": data.get("picture", "/default-profile.jpg")
    }
    PENDING_USERS[email] = pending_user
    USER_COUNTER += 1

    print(f"[MOCK] Signup request submitted for {email}. Pending admin approval.")
    return jsonify({"message": "Signup request submitted. Await admin approval."}), 201

@ui_mock_bp.route('/auth/forgot-password', methods=['POST'])
def forgot_password():
    """ For your ForgotPassword.js which calls /auth/forgot-password with {email}. 
        In a real system, you'd send an email with a reset link. 
        Here, we'll just respond with success if the user exists. """
    data = request.get_json()
    email = data.get("email")
    if not email:
        return jsonify({"error": "Email is required."}), 400
    if email not in MOCK_USERS:
        return jsonify({"error": "User not found."}), 404

    print(f"[MOCK] Forgot password request for {email}. Would send reset link via email.")
    return jsonify({"message": "Reset link sent to your email."}), 200

@ui_mock_bp.route('/auth/update-password', methods=['POST'])
def update_password():
    """
    Called by ResetPassword.js with:
      { oldPassword, newPassword }
    The user must have a valid token in localStorage, but for the mock,
    we'll skip the token check or do a simplified version.
    """
    data = request.get_json()
    old_password = data.get("oldPassword")
    new_password = data.get("newPassword")
    # In your real code, you'd also verify the token to find the correct user.
    # We'll just assume a single user for the mock, or we can pass token for a real check.

    # This is naive; let's assume the user has a token stored:
    # e.g. token -> email
    token = data.get("token")
    if not token or token not in USER_TOKENS:
        return jsonify({"error": "Invalid token."}), 401
    email = USER_TOKENS[token]
    user = MOCK_USERS.get(email)
    if not user:
        return jsonify({"error": "User not found."}), 404

    # Check old password
    if not bcrypt.checkpw(old_password.encode("utf-8"), user["password_hash"].encode("utf-8")):
        return jsonify({"error": "Old password is incorrect."}), 400

    # Validate new password
    valid, msg = validate_password(new_password, user.get("previous_passwords", []))
    if not valid:
        return jsonify({"error": msg}), 400

    # Save old password hash, update with new
    user.setdefault("previous_passwords", []).append(user["password_hash"])
    user["password_hash"] = bcrypt.hashpw(new_password.encode("utf-8"), bcrypt.gensalt()).decode("utf-8")

    print(f"[MOCK] Password updated for {email}.")
    return jsonify({"message": "Password updated successfully."}), 200

# --- ADMIN ENDPOINTS ---

@ui_mock_bp.route('/admin/approve_user', methods=['POST'])
def approve_user():
    data = request.get_json()
    email = data.get("email")
    if not email:
        return jsonify({"error": "Email is required."}), 400
    pending_user = PENDING_USERS.pop(email, None)
    if not pending_user:
        return jsonify({"error": "No pending request for this email."}), 404

    role = data.get("role", "regular")
    pending_user["role"] = role
    pending_user["active"] = True
    MOCK_USERS[email] = pending_user

    print(f"[MOCK] Admin approved user {email}.")
    return jsonify({"message": f"User {email} approved and activated."}), 200

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
    user["active"] = False
    return jsonify({"message": f"User {email} suspended."}), 200

@ui_mock_bp.route('/admin/update_user', methods=['POST'])
def update_user():
    data = request.get_json()
    email = data.get("email")
    if not email:
        return jsonify({"error": "Email is required."}), 400
    user = MOCK_USERS.get(email)
    if not user:
        return jsonify({"error": "User not found."}), 404

    # Allowed updates
    for field in ["first_name", "last_name", "address", "role"]:
        if field in data:
            user[field] = data[field]

    return jsonify({"message": f"User {email} updated successfully."}), 200

@ui_mock_bp.route('/admin/view_users', methods=['GET'])
def view_users():
    return jsonify({"users": list(MOCK_USERS.values())}), 200

@ui_mock_bp.route('/admin/report_expired_passwords', methods=['GET'])
def report_expired_passwords():
    expired = []
    now = datetime.datetime.now()
    for user in MOCK_USERS.values():
        created_at = datetime.datetime.fromisoformat(user["created_at"])
        if (now - created_at).days >= 90:
            expired.append(user)
    return jsonify({"expired_users": expired}), 200

@ui_mock_bp.route('/admin/send_email', methods=['POST'])
def admin_send_email():
    data = request.get_json()
    if "email" not in data or "subject" not in data or "body" not in data:
        return jsonify({"error": "email, subject, and body are required"}), 400
    print(f"[MOCK] Email to {data['email']} with subject '{data['subject']}' sent.")
    return jsonify({"message": "Email sent."}), 200
