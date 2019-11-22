from app import db


class User(db.Model):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), unique=True)
    password = db.Column(db.String(100))
    # articles = db.relationship('Article', backref='user', lazy='dynamic')

    def __init__(self, username, password):
        self.username = username
        self.password = password

    def add_user(self):
        with db.auto_commit_db():
            db.session.add(self)


class Article(db.Model):
    __tablename__ = 'articles'
    id = db.Column(db.Integer, primary_key=True)
    # user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    title = db.Column(db.String(100))
    text = db.Column(db.Text)

    def __init__(self, id, title, text):
        self.id = id
        self.title = title
        self.text = text

    def add_article(self):
        with db.auto_commit_db():
            db.session.add(self)

    def delete_article(self):
        with db.auto_commit_db():
            db.session.delete(self)
