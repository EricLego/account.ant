from app.extensions import db

class Token(db.Model):
    __tablename__ = "Tokens"

    token_id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("Users.user_id"), nullable=False)
    token_hash = db.Column(db.String(255), nullable=False)
    creation_time = db.Column(db.DateTime, nullable=False)
    expiry_time = db.Column(db.DateTime, nullable=False)

    user = db.relationship("User", back_populates="tokens")

    def __repr__(self):
        return f"<Token {self.token_id}>"
