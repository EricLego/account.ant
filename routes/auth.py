from flask import Blueprint, request, jsonify
from config.db_config import get_db_connection
from models.user import User
import jwt
import datetime
from werkzeug.security import check_password_hash

auth_bp = Blueprint('auth', __name__)
SECRET_KEY = "your_secret_key"

@auth_bp.route('/auth/login', methods=['POST'])
def login():
    data = request.get_json()
    email = data.get('email')
    password = data.get('password')

    if not email or not password:
        return jsonify({"message": "Email and password are required"}), 400

    db = get_db_connection()
    user = db.query(User).filter_by(email=email).first()
    
    if not user or not user.verify_password(password):
        db.close()
        return jsonify({"message": "Invalid credentials"}), 401

    if not user.status:  # Check `status` instead of `is_active`
        db.close()
        return jsonify({"message": "Account is suspended"}), 403

    token = jwt.encode({
        'sub': user.email,
        'name': f"{user.first_name} {user.last_name}",
        'role': user.role,
        'exp': datetime.datetime.utcnow() + datetime.timedelta(hours=1)
    }, SECRET_KEY, algorithm='HS256')

    db.close()
    return jsonify({"token": token, "role": user.role, "name": f"{user.first_name} {user.last_name}"})
