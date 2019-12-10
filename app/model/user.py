from app import db


class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), unique=True)
    password = db.Column(db.String(100))
    group_id = db.Column(db.Integer)
    # articles = db.relationship('Article', backref='user', lazy='dynamic')

    def __init__(self, username, password, group_id):
        self.username = username
        self.password = password
        self.group_id = group_id

    def add_user(self):
        with db.auto_commit_db():
            db.session.add(self)

    def update_user(self):
        with db.auto_commit_db():
            pass