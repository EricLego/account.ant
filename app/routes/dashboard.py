from flask import Blueprint, jsonify, request
from app.utils.auth import token_required  # Assumes token_required decorator is implemented
from app.models.user import User

dashboard_bp = Blueprint("dashboard", __name__, url_prefix="/dashboard")

@dashboard_bp.route("/", methods=["GET"])
@token_required
def get_dashboard():
    return jsonify({
        "message": f"Welcome to your dashboard!",
        "user_id": request.user_id,
        "role": request.user_role
    }), 200
