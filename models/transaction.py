from sqlalchemy import Column, Integer, Date, Numeric, ForeignKey
from models import Base

class Transaction(Base):
    __tablename__ = "Transactions"

    transaction_id = Column(Integer, primary_key=True, autoincrement=True)
    account_no = Column(Integer, ForeignKey("Accounts.account_no"), nullable=False)
    date = Column(Date, nullable=False)
    amount = Column(Numeric(10, 2), nullable=False)
