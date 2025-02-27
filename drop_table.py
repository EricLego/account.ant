from config.db_config import get_db_connection
from sqlalchemy.sql import text

def drop_table():
    """Prompts the user for a table name and drops it if it exists."""
    db = get_db_connection()
    if not db:
        print("Database connection failed.")
        return
    
    try:
        # Ask the user for the table name
        table_name = input("Enter the name of the table to drop: ").strip()

        # Confirm before executing the drop command
        confirm = input(f"Are you sure you want to drop the table '{table_name}'? (yes/no): ").strip().lower()
        if confirm != "yes":
            print("Operation cancelled.")
            return

        # Execute DROP TABLE command
        db.execute(text(f"DROP TABLE IF EXISTS {table_name}"))
        db.commit()
        print(f"Table '{table_name}' dropped successfully.")

    except Exception as e:
        print(f"Error dropping table: {e}")

    finally:
        db.close()

if __name__ == "__main__":
    drop_table()
