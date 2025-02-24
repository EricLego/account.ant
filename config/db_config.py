import pyodbc
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Retrieve database credentials from .env
DB_DRIVER = os.getenv("DB_DRIVER")
DB_SERVER = os.getenv("DB_SERVER")
DB_NAME = os.getenv("DB_NAME")
DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")
DB_ENCRYPT = os.getenv("DB_ENCRYPT", "yes")
DB_TRUST_SERVER_CERT = os.getenv("DB_TRUST_SERVER_CERT", "no")
DB_TIMEOUT = os.getenv("DB_TIMEOUT", "30")

# Check for missing credentials
MISSING_VARS = [var for var in ["DB_DRIVER", "DB_SERVER", "DB_NAME", "DB_USER", "DB_PASSWORD"] if not os.getenv(var)]
if MISSING_VARS:
    raise ValueError(f"Missing required environment variables: {', '.join(MISSING_VARS)}. Please check your .env file.")

# Construct the connection string dynamically
DB_CONNECTION_STRING = f"""
    Driver={DB_DRIVER};
    Server={DB_SERVER};
    Database={DB_NAME};
    Uid={DB_USER};
    Pwd={DB_PASSWORD};
    Encrypt={DB_ENCRYPT};
    TrustServerCertificate={DB_TRUST_SERVER_CERT};
    Connection Timeout={DB_TIMEOUT};
"""

def get_db_connection():
    """
    Establishes a connection to the SQL Server database.

    To do:
    1. Ensure all database credentials are properly set in `.env`.
    2. Verify that the ODBC Driver 18 for SQL Server is installed.
    3. Handle connection failures gracefully.
    """
    try:
        connection = pyodbc.connect(DB_CONNECTION_STRING)
        return connection
    except pyodbc.Error as e:
        print(f"Error connecting to database: {e}")
        return None

def get_cursor():
    """
    Returns a new cursor object for executing SQL queries.

    To do:
    1. Retrieve a database connection.
    2. Return a cursor object if the connection is successful.
    3. Handle failures by returning None.
    """
    connection = get_db_connection()
    if connection:
        return connection.cursor()
    return None

def init_db():
    """
    Initializes the database by creating necessary tables if they do not exist.

    To do:
    1. Ensure the database is accessible.
    2. Create the `users` table if it does not exist.
    3. Commit the changes and close the connection.
    """
    connection = get_db_connection()
    if not connection:
        print("Database connection failed. Cannot initialize database.")
        return

    cursor = connection.cursor()

    # Create the users table if it doesn't exist
    cursor.execute("""
        IF NOT EXISTS (SELECT * FROM sysobjects WHERE name='users' AND xtype='U')
        CREATE TABLE users (
            id INT IDENTITY(1,1) PRIMARY KEY,
            first_name NVARCHAR(50) NOT NULL,
            last_name NVARCHAR(50) NOT NULL,
            email NVARCHAR(100) UNIQUE NOT NULL,
            password_hash NVARCHAR(255) NOT NULL,
            role NVARCHAR(20) NOT NULL CHECK (role IN ('admin', 'manager', 'accountant')),
            is_active BIT DEFAULT 1
        );
    """)

    # Commit changes and close connection
    connection.commit()
    cursor.close()
    connection.close()
    print("Database initialized successfully.")
