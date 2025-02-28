import jwt
from passlib.context import CryptContext
from datetime import datetime, timedelta, timezone
import os
from dotenv import load_dotenv
from flask_sqlalchemy import SQLAlchemy

from app.models import db

class Password(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    hashed_password = db.Column(db.String(255), nullable=False)

    def __repr__(self):
        return f"<Password {self.id}>"

# Load environment variables
load_dotenv()

# Encryption details
SECRET_KEY = os.getenv("SECRET_KEY", "default_secret")
REFRESH_SECRET_KEY = os.getenv("REFRESH_SECRET_KEY", "default_refresh_secret")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30
REFRESH_TOKEN_EXPIRE_MINUTES = 30

pass_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

class Token:
    access_token: str
    refresh_token: str
    token_type: str

def verify_password(plain, hashed):
    return pass_context.verify(plain, hashed)

def hash_pass(plain):
    return pass_context.hash(plain)

def get_user(username: str):
    from config.db_config import get_db_connection
    from app.models import db
    db_conn = get_db_connection()
    cursor = db_conn.cursor()
    # Ensure table name matches lowercase 'users'
    cursor.execute("SELECT * FROM users WHERE username=%s", (username,))
    login_row = cursor.fetchone()
    db_conn.close()
    return login_row if login_row else False

def auth_user(username: str, password: str):
    user = get_user(username)
    if not user or not verify_password(password, user.password_hash):
        return None

    access_token_data = {"sub": user.user_id}
    refresh_token_data = {"sub": user.user_id}

    access_token = create_token(
        access_token_data,
        SECRET_KEY,
        timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    )
    refresh_token = create_token(
        refresh_token_data,
        REFRESH_SECRET_KEY,
        timedelta(minutes=REFRESH_TOKEN_EXPIRE_MINUTES)
    )

    from app.models import AccessToken, RefreshToken
    access_token_entry = AccessToken(
        user_id=user.user_id,
        token_hash=access_token,
        creation_time=datetime.now(timezone.utc),
        expiry_time=datetime.now(timezone.utc) + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    )
    refresh_token_entry = RefreshToken(
        user_id=user.user_id,
        token_hash=refresh_token,
        creation_time=datetime.now(timezone.utc),
        expiry_time=datetime.now(timezone.utc) + timedelta(minutes=REFRESH_TOKEN_EXPIRE_MINUTES)
    )

    db.session.add(access_token_entry)
    db.session.add(refresh_token_entry)
    db.session.commit()

    return user, access_token, refresh_token

def create_token(data: dict, secret, lifetime: timedelta):
    payload = data.copy()
    expire = datetime.now(timezone.utc) + lifetime
    payload.update({"exp": expire})
    return jwt.encode(payload, secret, algorithm=ALGORITHM)
