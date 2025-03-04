from app import create_app
from app.models import db
from sqlalchemy import text

# Create the Flask app
app = create_app()

# Run database connection test inside app context
with app.app_context():
    try:
        print(" Database URL:", db.engine.url)

        # Query the database for existing tables
        result = db.session.execute(text("SELECT TABLE_NAME FROM INFORMATION_SCHEMA.TABLES")).fetchall()
        
        # Print table names
        print(" Tables in database:")
        for row in result:
            print(row[0])

    except Exception as e:
        print(" Database connection error:", str(e))
