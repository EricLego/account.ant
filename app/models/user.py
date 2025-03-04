from app.extensions import db
from werkzeug.security import generate_password_hash, check_password_hash

class User(db.Model):
    __tablename__ = "Users"

    user_id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(32), nullable=False)
    last_name = db.Column(db.String(32), nullable=False)
    birth_date = db.Column(db.Date, nullable=False)
    email = db.Column(db.String(64), unique=True, nullable=False)
    hire_date = db.Column(db.Date, nullable=False)
    role = db.Column(db.Integer, nullable=False)
    status = db.Column(db.Boolean, nullable=False, default=True)
    suspend_start = db.Column(db.Date, nullable=True)
    suspend_end = db.Column(db.Date, nullable=True)
    password_hash = db.Column(db.String(255), nullable=False)

    accounts = db.relationship("Account", back_populates="user", cascade="all, delete-orphan")
    transactions = db.relationship("Transaction", back_populates="user")
    events = db.relationship("Event", back_populates="user")
    tokens = db.relationship("Token", back_populates="user", cascade="all, delete-orphan")
    security_questions = db.relationship("SecurityQuestion", back_populates="user")

    def __repr__(self):
        return f"<User {self.first_name} {self.last_name}>"

    @staticmethod
    def hash_password(password):
        return generate_password_hash(password)

    @staticmethod
    def verify_password(self, password):
        return check_password_hash(self.password_hash, password)