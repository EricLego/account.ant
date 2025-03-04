from app.extensions import db
from sqlalchemy import Column, Integer, Numeric, DateTime, ForeignKey

class Transaction(db.Model):
    __tablename__ = "transactions"
    __table_args__ = {"extend_existing": True}

    transaction_id = Column(Integer, primary_key=True, autoincrement=True)
    account_no = Column(Integer, ForeignKey("accounts.account_no"), nullable=False)
    user_id = Column(Integer, ForeignKey("Users.user_id"), nullable=False)
    transaction_datetime = Column(DateTime, nullable=False)  # renamed to avoid conflict with datetime module
    amount = Column(Numeric(10, 2), nullable=False)

    user = db.relationship("User", back_populates="transactions")
    account = db.relationship("Account", back_populates="transactions")

    def __repr__(self):
        return f"<Transaction {self.transaction_id}: Amount {self.amount}>"
