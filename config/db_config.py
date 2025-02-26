import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv
from models import Base  # ✅ FIXED: Import Base from models/__init__.py

# Load environment variables
load_dotenv()

# Retrieve database credentials
DB_DRIVER = os.getenv("DB_DRIVER", "ODBC Driver 18 for SQL Server")
DB_SERVER = os.getenv("DB_SERVER")
DB_NAME = os.getenv("DB_NAME")
DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")

# Correct SQLAlchemy connection string for Azure SQL Server using pyodbc
import urllib
params = urllib.parse.quote_plus(
    f"DRIVER={DB_DRIVER};"
    f"SERVER={DB_SERVER},1433;"
    f"DATABASE={DB_NAME};"
    f"UID={DB_USER};"
    f"PWD={DB_PASSWORD};"
    f"Encrypt=yes;"
    f"TrustServerCertificate=no;"
    f"Connection Timeout=30;"
)

SQLALCHEMY_DATABASE_URL = f"mssql+pyodbc:///?odbc_connect={params}"

# Create SQLAlchemy engine & session
engine = create_engine(SQLALCHEMY_DATABASE_URL, echo=True, fast_executemany=True)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def get_db_connection():
    """Returns a new database session."""
    return SessionLocal()

def init_db():
    """Initializes the database by creating necessary tables."""
    from models.user import User  # FIXED FINALLY HOLY CHRIST
    Base.metadata.create_all(bind=engine)
    print("Database initialized successfully.")
