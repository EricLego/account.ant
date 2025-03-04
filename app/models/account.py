from app.extensions import db
from sqlalchemy import Column, Integer, String, Date, ForeignKey, Text, Numeric, Boolean

class Account(db.Model):
    __tablename__ = "accounts"
    __table_args__ = {"extend_existing": True}

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
    order = Column(String(50), nullable=True)  # Consider renaming if it conflicts with reserved words.
    statement = Column(Text, nullable=True)
    comment = Column(Text, nullable=True)

    user = db.relationship("User", back_populates="accounts")
    events = db.relationship("Event", back_populates="account")
    transactions = db.relationship(
        "Transaction",
        back_populates="account",
        cascade="all, delete-orphan",
        lazy="dynamic"
    )

    def __repr__(self):
        return f"<Account {self.account_no}: {self.account_name}>"
