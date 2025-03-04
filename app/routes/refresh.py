@auth_bp.route('/auth/refresh', methods=['POST'])
def refresh_token():
    data = request.get_json()
    token = data.get("token")

    if not token:
        return jsonify({"error": "Token is required"}), 400

    try:
        decoded = jwt.decode(token, SECRET_KEY, algorithms=["HS256"], options={"verify_exp": False})
        new_token = jwt.encode({
            "sub": decoded["sub"],
            "name": decoded["name"],
            "role": decoded["role"],
            "exp": datetime.datetime.utcnow() + datetime.timedelta(hours=EXPIRY_HOURS)
        }, SECRET_KEY, algorithm="HS256")

        return jsonify({"token": new_token}), 200

    except InvalidTokenError:
        return jsonify({"error": "Invalid token"}), 401
