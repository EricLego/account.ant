from sqlalchemy import text
from config.db_config import get_db_connection

try:
    session = get_db_connection()
    result = session.execute(text("SELECT 1")).fetchone()
    print("✅ Database connection successful:", result)
    session.close()
except Exception as e:
    print("❌ Database connection failed:", e)
