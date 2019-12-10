from app import db


class ClassName(db.Model):
    __tablename__ = 'classnames'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))

    def delete_classname(self):
        with db.auto_commit_db():
            db.session.delete(self)

    def add_classname(self):
        with db.auto_commit_db():
            db.session.add(self)