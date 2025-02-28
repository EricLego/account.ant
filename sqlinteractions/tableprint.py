from config.db_config import get_db_connection
from sqlalchemy.sql import text

db = get_db_connection()
query = text("SELECT TABLE_NAME FROM INFORMATION_SCHEMA.TABLES WHERE TABLE_TYPE = 'BASE TABLE';")
result = db.execute(query)

print([row[0] for row in result])

db.close()
