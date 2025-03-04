from app.extensions import db

class Event(db.Model):
    __tablename__ = "Events"

    event_id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("Users.user_id"), nullable=False)
    account_no = db.Column(db.Integer, db.ForeignKey("Accounts.account_no"), nullable=False)
    datetime = db.Column(db.DateTime, nullable=False)
    before = db.Column(db.Numeric(18, 2), nullable=False)
    after = db.Column(db.Numeric(18, 2), nullable=False)

    user = db.relationship("User", back_populates="events")
    account = db.relationship("Account")

    def __repr__(self):
        return f"<Event {self.event_id}>"
