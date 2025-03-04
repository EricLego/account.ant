from flask import Flask
from dotenv import load_dotenv
import os

# Load environment variables early.
load_dotenv()


# Import configuration from our unified config file.
from app.config.config import Config

from app.extensions import db, migrate

def create_app():
    app = Flask(__name__)
    # app.config["SQLALCHEMY_DATABASE_URI"] = (
    # "mssql+pyodbc:///?odbc_connect="
    # "Driver%3D%7BODBC+Driver+18+for+SQL+Server%7D%3B"
    # "Server%3Dtcp%3Aaccount-ant.database.windows.net%2C1433%3B"
    # "Database%3Daccount-ant-employee%3BUid%3DworkerAnt%3BPwd%3DforTheColony01%21%21%3B"
    # "Encrypt%3Dyes%3BTrustServerCertificate%3Dno%3BConnection+Timeout%3D30%3B"
    # )
    # Load configuration from our config class.
    app.config.from_object(Config)
    
    # Debug: Confirm that the SQLALCHEMY_DATABASE_URI is loaded.
    # print("App SQLALCHEMY_DATABASE_URI:", app.config.get("SQLALCHEMY_DATABASE_URI"))
    
    # Initialize extensions.
    db.init_app(app)
    migrate.init_app(app, db)
    
    # Import models within app context to avoid circular imports.
    with app.app_context():
        from app.models.user import User
        from app.models.account import Account
        from app.models.event import Event
        from app.models.transaction import Transaction
        db.create_all()
    
    # Register blueprints.
    from app.routes.auth import auth_bp
    from app.routes.user import user_bp
    
    app.register_blueprint(auth_bp)
    app.register_blueprint(user_bp)
    
    return app

app = create_app()
