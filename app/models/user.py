from app.extensions import db
from sqlalchemy import Column, Integer, String, Boolean, Date
import bcrypt

class User(db.Model):
    __tablename__ = "users"
    __table_args__ = {"extend_existing": True}

    user_id = Column(Integer, primary_key=True, autoincrement=True)
    first_name = Column(String(50), nullable=False)
    last_name = Column(String(50), nullable=False)
    birth_date = Column(Date, nullable=True)
    email = Column(String(100), unique=True, nullable=False)
    hire_date = Column(Date, nullable=True)
    role = Column(Integer, nullable=False)
    status = Column(Boolean, default=True)
    suspend_start = Column(Date, nullable=True)
    suspend_end = Column(Date, nullable=True)
    password_hash = Column(String(255), nullable=False)

    # Use simple class names for relationship references
    accounts = db.relationship(
        "Account",
        back_populates="user",
        cascade="all, delete-orphan",
        lazy="dynamic"
    )
    access_tokens = db.relationship(
        "AccessToken",
        back_populates="user",
        cascade="all, delete-orphan",
        lazy="dynamic"
    )
    refresh_tokens = db.relationship(
        "RefreshToken",
        back_populates="user",
        cascade="all, delete-orphan",
        lazy="dynamic"
    )
    transactions = db.relationship(
        "Transaction",
        back_populates="user",
        cascade="all, delete-orphan",
        lazy="dynamic"
    )
    events = db.relationship(
        "Event",
        back_populates="user",
        cascade="all, delete-orphan",
        lazy="dynamic"
    )

    @staticmethod
    def hash_password(password: str) -> str:
        return bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt()).decode("utf-8")

    def verify_password(self, password: str) -> bool:
        return bcrypt.checkpw(password.encode("utf-8"), self.password_hash.encode("utf-8"))

    def __repr__(self):
        return f"<User {self.user_id}: {self.first_name} {self.last_name} ({'Active' if self.status else 'Suspended'})>"
