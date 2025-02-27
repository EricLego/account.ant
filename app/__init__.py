from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
import os
from dotenv import load_dotenv
from app.extensions import db, migrate

# Load environment variables
load_dotenv()

db = SQLAlchemy()
migrate = Migrate()

def create_app():
    app = Flask(__name__)

    # Database configuration
    app.config["SECRET_KEY"] = os.getenv("SECURITY_KEY", "default_secret_key")
    app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv("DATABASE_URL", "sqlite:///default.db")
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    # Initialize extensions
    db.init_app(app)
    migrate.init_app(app, db)

    # Import models inside the function to avoid circular imports
    with app.app_context():
        from models.user import User
        from models.account import Account
        from models.event import Event
        from models.transaction import Transaction
        db.create_all()

    # Register blueprints
    from routes.auth import auth_bp
    from routes.user import user_bp
    app.register_blueprint(auth_bp)
    app.register_blueprint(user_bp)

    return app

app = create_app()
