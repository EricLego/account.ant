from app.extensions import db

class SysDiagram(db.Model):
    __tablename__ = "sysdiagrams"

    diagram_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(128), nullable=False, unique=True)
    principal_id = db.Column(db.Integer, nullable=False)
    version = db.Column(db.Integer, nullable=True)
    definition = db.Column(db.LargeBinary, nullable=True)

    def __repr__(self):
        return f"<SysDiagram {self.name}>"
