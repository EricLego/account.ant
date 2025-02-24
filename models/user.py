from sqlalchemy import Column, Integer, String, Boolean
from config.db_config import Base
import bcrypt

class User(Base):
    """
    User model representing application users.

    To do:
    1. Ensure the database is properly connected (`init_db()` in `db_config.py`).
    2. Always hash passwords before storing them.
    3. Verify that role options match application requirements.
    """
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, autoincrement=True)
    first_name = Column(String(50), nullable=False)
    last_name = Column(String(50), nullable=False)
    email = Column(String(100), unique=True, nullable=False)
    password_hash = Column(String(255), nullable=False)
    role = Column(String(20), nullable=False)  # Options: 'admin', 'manager', 'accountant'
    is_active = Column(Boolean, default=True)

    @staticmethod
    def hash_password(password):
        """
        Hashes a password for secure storage.

        To do:
        1. Use bcrypt to generate a secure password hash.
        2. Ensure password is encoded in UTF-8 before hashing.
        3. Return the hashed password as a decoded string.
        """
        return bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt()).decode("utf-8")

    def verify_password(self, password):
        """
        Verifies a password against the stored hash.

        To do:
        1. Encode the provided password in UTF-8.
        2. Compare it with the stored hashed password.
        3. Return True if the password matches, False otherwise.
        """
        return bcrypt.checkpw(password.encode("utf-8"), self.password_hash.encode("utf-8"))
