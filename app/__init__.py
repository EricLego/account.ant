from flask import Flask
from dotenv import load_dotenv
from app.config.config import Config
from app.extensions import db, migrate
from flask_cors import CORS

# Load environment variables early.
load_dotenv()

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)  # Load configuration
    CORS(app)

    db.init_app(app)
    migrate.init_app(app, db)

    with app.app_context():
        from app.models import user, account, event, transaction, password, security_questions
        db.create_all()

    from app.routes.auth import auth_bp
    from app.routes.user import user_bp
    from app.routes.dashboard import dashboard_bp

    app.register_blueprint(auth_bp)
    app.register_blueprint(user_bp)
    app.register_blueprint(dashboard_bp)

    return app

if __name__ == "__main__":
    app = create_app()
