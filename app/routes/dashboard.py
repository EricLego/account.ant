from flask import Blueprint, jsonify, request
from app.utils.auth import token_required  # Assumes token_required decorator is implemented
from app.models.user import User

dashboard_bp = Blueprint("dashboard", __name__, url_prefix="/dashboard")

@dashboard_bp.route("/", methods=["GET"])
@token_required
def get_dashboard():
    user = User.query.get(request.user_id)
    
    if not user:
        return jsonify({"error": "User not found"}), 404

    return jsonify({
        "message": f"Welcome to your dashboard, {user.first_name}!",
        "role": user.role
    }), 200
