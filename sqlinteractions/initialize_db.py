from config.db_config import get_db_connection
from models import Base

# Create all tables in the database
db = get_db_connection()
Base.metadata.create_all(bind=db.get_bind())
db.close()
