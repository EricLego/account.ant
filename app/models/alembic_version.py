from app.extensions import db

#keeps track of migrations.
class AlembicVersion(db.Model):
    __tablename__ = "alembic_version"

    version_num = db.Column(db.String(32), primary_key=True)

    def __repr__(self):
        return f"<AlembicVersion {self.version_num}>"
