import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

class Config:
    """
    Stores application configuration settings.
    
    Sections to update:
    - `DATABASE_URL` Use your actual database connection.
    - `DEBUG`  Set to False in production.
    - Maybe add SMTP         
    """

    # 🔹 Update this for production security
    SECRET_KEY = os.getenv("SECRET_KEY", "6998950996c4bdbf1f4391bb011a27427a490df130aac3796ba399101e054bf6")

    # 🔹 Database Configuration (Change to your DB credentials)
    DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///db.sqlite3")  # Default: SQLite

    # 🔹 Debug Mode (False for Production)
    DEBUG = os.getenv("DEBUG", "True").lower() == "true"