from app.extensions import db


class Transaction(db.Model):
    __tablename__ = "Transactions"

    transaction_id = db.Column(db.Integer, primary_key=True)
    account_no = db.Column(db.Integer, db.ForeignKey("Accounts.account_no"), nullable=False)
    date = db.Column(db.Date, nullable=False)
    amount = db.Column(db.Numeric(18, 2), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey("Users.user_id"), nullable=False)

    user = db.relationship("User", back_populates="transactions")
    account = db.relationship("Account", back_populates="transactions")

    def __repr__(self):
        return f"<Transaction {self.transaction_id} - {self.amount}>"
