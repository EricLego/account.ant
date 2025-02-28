import os
from flask import Flask
from dotenv import load_dotenv
from app.extensions import db, migrate

def create_app():
    # Load environment variables
    load_dotenv()

    app = Flask(__name__)

    # Basic config
    app.config["SECRET_KEY"] = os.getenv("SECRET_KEY", "default_secret_key")
    # If you want to build the full DB URI from .env variables, do so here; 
    # for now, just read DATABASE_URL or default to SQLite:
    app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv("DATABASE_URL", "sqlite:///default.db")
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    # Initialize database + migration
    db.init_app(app)
    migrate.init_app(app, db)

    # Import models within app_context to avoid circular imports
    with app.app_context():
        from app.models.user import User
        from app.models.account import Account
        from app.models.event import Event
        from app.models.transaction import Transaction
        db.create_all()

    # Register blueprints
    from app.routes.auth import auth_bp
    from app.routes.user import user_bp
    from app.routes.ui_mock_routes import ui_mock_bp

    app.register_blueprint(auth_bp)
    app.register_blueprint(user_bp)
    app.register_blueprint(ui_mock_bp)  # So /auth/* routes from ui_mock are active

    return app

# Create a global 'app' instance if you want to run via `python -m flask` or `flask run`
app = create_app()
