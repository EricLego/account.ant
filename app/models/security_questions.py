from app.extensions import db

class SecurityQuestion(db.Model):
    __tablename__ = "Security_Questions"

    question_id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("Users.user_id"), nullable=False)
    question = db.Column(db.String(64), nullable=False)
    answer = db.Column(db.String(64), nullable=False)

    user = db.relationship("User", back_populates="security_questions")

    def __repr__(self):
        return f"<SecurityQuestion {self.question}>"
