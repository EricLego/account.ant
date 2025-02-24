from flask import Blueprint, request, jsonify
from werkzeug.security import check_password_hash
import jwt
import datetime

# Werkzeug security is used for password hashing and checking. Might replace.

auth_bp = Blueprint('auth', __name__)

# Mock user data for demonstration purposes
users = {
    "user@example.com": {
        "password": "hashed_password",  # Replace with actual hashed password
        "name": "Eric Legos"
    }
}

SECRET_KEY = 'your_secret_key'  # Replace with your actual secret key

@auth_bp.route('/auth/login', methods=['POST'])
def login():
    data = request.get_json()
    email = data.get('email')
    password = data.get('password')

    if not email or not password:
        return jsonify({"message": "Email and password are required"}), 400

    user = users.get(email)
    if user and check_password_hash(user['password'], password):
        token = jwt.encode({
            'sub': email,
            'name': user['name'],
            'exp': datetime.datetime.utcnow() + datetime.timedelta(hours=1)
        }, SECRET_KEY, algorithm='HS256')

        return jsonify({"token": token})

    return jsonify({"message": "Invalid credentials"}), 401