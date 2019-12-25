from app import db
import time


class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), unique=True)
    password = db.Column(db.String(100))
    group_id = db.Column(db.Integer)

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
    labels = db.Column(db.String(100))
    classname_id = db.Column(db.Integer)
    time = db.Column(db.Integer)

    def __init__(self, id, title, text, classname_id, labels, view_number, like_number, comment_number, time):
        self.id = id
        self.title = title
        self.text = text
        self.view_number = view_number
        self.like_number = like_number
        self.comment_number = comment_number
        self.classname_id = classname_id
        self.labels = labels
        self.time = time

    def add_article(self):
        with db.auto_commit_db():
            self.time = int(time.time())
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
            self.time = int(time.time())


class ClassName(db.Model):
    __tablename__ = 'classnames'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))

    def __init__(self,name):
        self.name = name

    def delete_classname(self):
        with db.auto_commit_db():
            db.session.delete(self)

    def add_classname(self):
        with db.auto_commit_db():
            db.session.add(self)


class Comment(db.Model):
    __tablename__ = 'comments'
    id = db.Column(db.Integer, primary_key=True)
    article_id = db.Column(db.Integer, db.ForeignKey('articles.id'))
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    text = db.Column(db.Text)
    timestamp = db.Column(db.Integer)

    def __init__(self, id, article_id, user_id, text, timestamp):
        self.id = id
        self.article_id = article_id
        self.user_id = user_id
        self.text = text
        self.timestamp = timestamp

    def add_comment(self):
        with db.auto_commit_db():
            db.session.add(self)