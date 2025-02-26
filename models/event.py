from sqlalchemy import Column, Integer, DateTime, Numeric, ForeignKey
from models import Base

class Event(Base):
    __tablename__ = "Events"

    event_id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey("Users.user_id"), nullable=False)
    account_no = Column(Integer, ForeignKey("Accounts.account_no"), nullable=False)
    datetime = Column(DateTime, nullable=False)
    before = Column(Numeric(10, 2), nullable=False)
    after = Column(Numeric(10, 2), nullable=False)
