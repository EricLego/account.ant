import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

class Config:
    """
    Stores application configuration settings.
    
    ⚠️ Sections to update:
    - `SECRET_KEY` → Change for security purposes.
    - `DATABASE_URL` → Use your actual database connection.
    - `DEBUG` → Set to False in production.
    - `SMTP Settings` → If email functionality is required.
    """

    # 🔹 Update this for production security
    SECRET_KEY = os.getenv("SECRET_KEY", "change_this_secret")

    # 🔹 Database Configuration (Change to your DB credentials)
    DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///db.sqlite3")  # Default: SQLite

    # 🔹 Debug Mode (False for Production)
    DEBUG = os.getenv("DEBUG", "True").lower() == "true"

    # 🔹 SMTP Configuration (Used for sending emails)
    SMTP_SERVER = os.getenv("SMTP_SERVER", "smtp.example.com")
    SMTP_PORT = int(os.getenv("SMTP_PORT", 587))
    SMTP_USER = os.getenv("SMTP_USER", "your_email@example.com")
    SMTP_PASSWORD = os.getenv("SMTP_PASSWORD", "your_secure_password")
