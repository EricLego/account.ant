from app.extensions import db

class Password(db.Model):
    __tablename__ = "Passwords"

    password_id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("Users.user_id"), nullable=False)
    creation_date = db.Column(db.Date, nullable=False)
    expiry_date = db.Column(db.Date, nullable=False)
    past_password = db.Column(db.Text, nullable=True)

    def __repr__(self):
        return f"<Password {self.password_id}>"
