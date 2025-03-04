from app.extensions import db

class Account(db.Model):
    __tablename__ = "Accounts"

    account_no = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("Users.user_id"), nullable=False)
    account_name = db.Column(db.String(32), nullable=False)
    description = db.Column(db.Text, nullable=False)
    normal_side = db.Column(db.Boolean, nullable=False)
    category = db.Column(db.String(32), nullable=False)
    subcategory = db.Column(db.String(32), nullable=False)
    date = db.Column(db.Date, nullable=False)
    initial_balance = db.Column(db.Numeric(18, 2), nullable=False)
    debit = db.Column(db.Numeric(18, 2), nullable=True)
    credit = db.Column(db.Numeric(18, 2), nullable=True)
    balance = db.Column(db.Numeric(18, 2), nullable=False)
    account_order = db.Column(db.Integer, nullable=False)
    statement = db.Column(db.Text, nullable=False)
    comment = db.Column(db.Text, nullable=True)

    user = db.relationship("User", back_populates="accounts")
    transactions = db.relationship("Transaction", back_populates="account", cascade="all, delete-orphan")

    def __repr__(self):
        return f"<Account {self.account_name}>"
