# config.py
import os
import urllib.parse
from dotenv import load_dotenv

load_dotenv()  # Loads variables from your .env file

# Read environment variables (with sensible defaults)
db_driver = os.environ.get("DB_DRIVER", "ODBC Driver 18 for SQL Server")
db_server = os.environ.get("DB_SERVER", "tcp:yourserver.database.windows.net,1433")
db_name = os.environ.get("DB_NAME", "your_db_name")
db_user = os.environ.get("DB_USER", "your_username")
db_password = os.environ.get("DB_PASSWORD", "your_password")
db_encrypt = os.environ.get("DB_ENCRYPT", "yes")
db_trust_cert = os.environ.get("DB_TRUST_SERVER_CERT", "no")
db_timeout = os.environ.get("DB_TIMEOUT", "30")

# Build the ODBC connection string
connection_string = (
    f"Driver={{{db_driver}}};"
    f"Server={db_server};"
    f"Database={db_name};"
    f"Uid={db_user};"
    f"Pwd={db_password};"
    f"Encrypt={db_encrypt};"
    f"TrustServerCertificate={db_trust_cert};"
    f"Connection Timeout={db_timeout};"
)

# URL-encode the connection string
params = urllib.parse.quote_plus(connection_string)

# Create the SQLAlchemy connection URI
SQLALCHEMY_DATABASE_URI = f"mssql+pyodbc:///?odbc_connect={params}"
