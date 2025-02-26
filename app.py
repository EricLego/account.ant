from flask import Flask
from routes.auth import auth_bp  # Import your route blueprints
from routes.user import user_bp

app = Flask(__name__)

# Register blueprints
app.register_blueprint(auth_bp)
app.register_blueprint(user_bp)

if __name__ == "__main__":
    app.run(debug=True)
