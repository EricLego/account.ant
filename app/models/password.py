import jwt
from passlib.context import CryptContext
from datetime import datetime, timedelta, timezone
import os
from dotenv import load_dotenv

from app.extensions import db

# Ensure environment variables are loaded.
load_dotenv()

# Encryption and token details
SECRET_KEY = os.getenv("SECRET_KEY", "default_secret")
REFRESH_SECRET_KEY = os.getenv("REFRESH_SECRET_KEY", "default_refresh_secret")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30
REFRESH_TOKEN_EXPIRE_MINUTES = 30

pass_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

class Password(db.Model):
    __tablename__ = "passwords"
    __table_args__ = {"extend_existing": True}

    id = db.Column(db.Integer, primary_key=True)
    hashed_password = db.Column(db.String(255), nullable=False)

    def __repr__(self):
        return f"<Password {self.id}>"

# Token data structure (optional, can be extended or converted to a dataclass)
class Token:
    access_token: str
    refresh_token: str
    token_type: str

def verify_password(plain: str, hashed: str) -> bool:
    return pass_context.verify(plain, hashed)

def hash_pass(plain: str) -> str:
    return pass_context.hash(plain)

def get_user(email: str):
    """
    Retrieve a user by email using the ORM.
    """
    from app.models.user import User
    return User.query.filter_by(email=email).first()

def auth_user(email: str, password: str):
    """
    Authenticate a user using email and password.
    Returns a tuple of (user, access_token, refresh_token) on success, or None on failure.
    """
    user = get_user(email)
    if not user or not user.verify_password(password):
        return None

    # Create token payloads
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

    # Import token models and store hashed tokens
    from app.models.accesstoken import AccessToken
    from app.models.refreshtoken import RefreshToken

    access_token_entry = AccessToken(
        user_id=user.user_id,
        token_hash=AccessToken.create_token_hash(access_token),
        creation_time=datetime.now(timezone.utc),
        expiry_time=datetime.now(timezone.utc) + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    )
    refresh_token_entry = RefreshToken(
        user_id=user.user_id,
        token_hash=RefreshToken.create_token_hash(refresh_token),
        creation_time=datetime.now(timezone.utc),
        expiry_time=datetime.now(timezone.utc) + timedelta(minutes=REFRESH_TOKEN_EXPIRE_MINUTES)
    )

    db.session.add(access_token_entry)
    db.session.add(refresh_token_entry)
    db.session.commit()

    return user, access_token, refresh_token

def create_token(data: dict, secret: str, lifetime: timedelta) -> str:
    """
    Create a JWT token with an expiration.
    """
    payload = data.copy()
    expire = datetime.now(timezone.utc) + lifetime
    payload.update({"exp": expire})
    return jwt.encode(payload, secret, algorithm=ALGORITHM)
