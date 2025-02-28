from app.extensions import db
from sqlalchemy import Column, Integer, Numeric, DateTime, ForeignKey

class Transaction(db.Model):
    __tablename__ = "transactions"
    __table_args__ = {"extend_existing": True}

    transaction_id = Column(Integer, primary_key=True, autoincrement=True)
    account_no = Column(Integer, ForeignKey("accounts.account_no"), nullable=False)
    user_id = Column(Integer, ForeignKey("users.user_id"), nullable=False)
    datetime = Column(DateTime, nullable=False)
    amount = Column(Numeric(10, 2), nullable=False)

    # Simple relationship references
    user = db.relationship("User", back_populates="transactions")
    account = db.relationship("Account", back_populates="transactions")
