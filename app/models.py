from app import db


class User(db.Model):
    __tablename__ = 'user'
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


class Article(db.Model):
    __tablename__ = 'articles'
    id = db.Column(db.Integer, primary_key=True)
    # user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    title = db.Column(db.String(100))
    text = db.Column(db.Text)
    view_number = db.Column(db.Integer)
    like_number = db.Column(db.Integer)
    comment_number = db.Column(db.Integer)

    def __init__(self, id, title, text, view_number, like_number, comment_number):
        self.id = id
        self.title = title
        self.text = text
        self.view_number = view_number
        self.like_number = like_number
        self.comment_number = comment_number

    def add_article(self):
        with db.auto_commit_db():
            db.session.add(self)

    def delete_article(self):
        with db.auto_commit_db():
            db.session.delete(self)

    def view_article(self):
        with db.auto_commit_db():
            self.view_number += 1

    def like_article(self):
        with db.auto_commit_db():
            self.like_number += 1

    def update_article(self):
        with db.auto_commit_db():
            pass