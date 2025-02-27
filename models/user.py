from sqlalchemy import Column, Integer, String, Boolean, Date, ForeignKey
import bcrypt
from models import Base

class User(Base):
    __tablename__ = "Users"

    user_id = Column(Integer, primary_key=True, autoincrement=True)
    first_name = Column(String(50), nullable=False)
    last_name = Column(String(50), nullable=False)
    birth_date = Column(Date, nullable=True)
    email = Column(String(100), unique=True, nullable=False)
    hire_date = Column(Date, nullable=True)
    role = Column(Integer, nullable=False)  # Stored as an int in DB
    status = Column(Boolean, default=True)
    suspend_start = Column(Date, nullable=True)
    suspend_end = Column(Date, nullable=True)
    password_hash = Column(String(255), nullable=False)

    @staticmethod
    def hash_password(password):
        return bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt()).decode("utf-8")

    def verify_password(self, password):
        return bcrypt.checkpw(password.encode("utf-8"), self.password_hash.encode("utf-8"))
