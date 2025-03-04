# app/config.py
import os
import urllib.parse
from dotenv import load_dotenv

load_dotenv()

def get_sqlalchemy_database_uri():
    db_driver = os.getenv("DB_DRIVER", "ODBC Driver 18 for SQL Server")
    db_server = os.getenv("DB_SERVER", "account-ant.database.windows.net")  # Removed `tcp:`
    db_port = "1433"  # Azure SQL default port
    db_name = os.getenv("DB_NAME", "account-ant-employee")
    db_user = os.getenv("DB_USER", "workerAnt")
    db_password = os.getenv("DB_PASSWORD", "forTheColony01!!")
    db_encrypt = os.getenv("DB_ENCRYPT", "yes")
    db_trust_cert = os.getenv("DB_TRUST_SERVER_CERT", "no")
    db_timeout = os.getenv("DB_TIMEOUT", "30")

    auth_method = os.getenv("DB_AUTH_METHOD", "password")  # Options: "password" or "azure_ad"

    if auth_method == "azure_ad":
        connection_string = (
            f"Driver={{{db_driver}}};"
            f"Server={db_server},{db_port};"
            f"Database={db_name};"
            f"Authentication=ActiveDirectoryDefault;"
            f"Encrypt={db_encrypt};"
            f"TrustServerCertificate={db_trust_cert};"
            f"Connection Timeout={db_timeout};"
        )
    else:
        connection_string = (
            f"Driver={{{db_driver}}};"
            f"Server={db_server},{db_port};"
            f"Database={db_name};"
            f"Uid={db_user};"
            f"Pwd={db_password};"
            f"Encrypt={db_encrypt};"
            f"TrustServerCertificate={db_trust_cert};"
            f"Connection Timeout={db_timeout};"
        )

    params = urllib.parse.quote_plus(connection_string)
    return f"mssql+pyodbc:///?odbc_connect={params}"

class Config:
    SECRET_KEY = os.getenv("SECRET_KEY", "default_secret_key")
    DEBUG = os.getenv("DEBUG", "True").lower() == "true"
    SQLALCHEMY_DATABASE_URI = get_sqlalchemy_database_uri()
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    JWT_EXPIRY_HOURS = int(os.getenv("JWT_EXPIRY_HOURS", 1))  # Default 1 hour


def get_db_connection():
    """Returns the database session."""
    from app import db
    return db.session
