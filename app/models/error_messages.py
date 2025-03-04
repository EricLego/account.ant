from app.extensions import db

class ErrorMessage(db.Model):
    __tablename__ = "Error_Messages"

    error_code = db.Column(db.Integer, primary_key=True)
    message = db.Column(db.Text, nullable=False)

    def __repr__(self):
        return f"<Error {self.error_code}>"
