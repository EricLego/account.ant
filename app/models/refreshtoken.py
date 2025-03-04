from app.extensions import db
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from datetime import datetime
import bcrypt

class RefreshToken(db.Model):
    __tablename__ = "refreshtokens"  # using lowercase table name
    __table_args__ = {"extend_existing": True}

    token_id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey("Users.user_id"), nullable=False)
    token_hash = Column(String(255), nullable=False)
    creation_time = Column(DateTime, default=datetime.utcnow, nullable=False)
    expiry_time = Column(DateTime, nullable=False)

    user = db.relationship("User", back_populates="refresh_tokens")

    def __repr__(self) -> str:
        return f"<RefreshToken user_id={self.user_id} token_id={self.token_id} expires={self.expiry_time}>"

    @staticmethod
    def create_token_hash(token: str) -> str:
        return bcrypt.hashpw(token.encode("utf-8"), bcrypt.gensalt()).decode("utf-8")

    def is_expired(self) -> bool:
        return datetime.utcnow() > self.expiry_time
