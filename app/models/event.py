from app.extensions import db
from sqlalchemy import Column, Integer, DateTime, Numeric, ForeignKey

class Event(db.Model):
    __tablename__ = "events"
    __table_args__ = {"extend_existing": True}

    event_id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey("users.user_id"), nullable=False)
    account_no = Column(Integer, ForeignKey("accounts.account_no"), nullable=False)
    datetime = Column(DateTime, nullable=False)
    before = Column(Numeric(10, 2), nullable=False)
    after = Column(Numeric(10, 2), nullable=False)

    user = db.relationship("User", back_populates="events")
    account = db.relationship("Account", back_populates="events")
