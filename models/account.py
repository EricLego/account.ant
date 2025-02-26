from sqlalchemy import Column, Integer, String, Date, ForeignKey, Text, Numeric, Boolean
from models import Base

class Account(Base):
    __tablename__ = "Accounts"

    account_no = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey("Users.user_id"), nullable=False)
    account_name = Column(String(50), nullable=False)
    description = Column(Text, nullable=True)
    normal_side = Column(Boolean, nullable=True)
    category = Column(String(50), nullable=False)
    subcategory = Column(String(50), nullable=True)
    date = Column(Date, nullable=False)
    initial_balance = Column(Numeric(10, 2), nullable=False)
    debit = Column(Numeric(10, 2), nullable=False)
    credit = Column(Numeric(10, 2), nullable=False)
    balance = Column(Numeric(10, 2), nullable=False)
    order = Column(String(50), nullable=True)
    statement = Column(Text, nullable=True)
    comment = Column(Text, nullable=True)
