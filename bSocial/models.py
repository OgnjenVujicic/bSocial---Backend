from datetime import datetime
from bSocial import db
from flask import jsonify

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(20), nullable=False)
    last_name = db.Column(db.String(20), nullable=False)
    username = db.Column(db.String(20), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    image_file = db.Column(db.String(20), nullable=False, default='default.jpg')
    password = db.Column(db.String(60), nullable=False)
    posts = db.relationship('Post', backref='author', lazy=True)

    def serialize(self):
        return {"id": self.id,
                "first_name": self.first_name,
                "last_name": self.last_name,
                "username": self.username,
                "email": self.email,
                "image_file": self.image_file}

    def __repr__(self):
        return f"User('{self.username}', '{self.email}', '{self.image_file}')"


class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    date_time = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    content = db.Column(db.Text, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    comments = db.relationship('Comment', backref='post', lazy=True)

    def serialize(self):
        return {"id": self.id,
                "title": self.title,
                "date_time": self.date_time,
                "content": self.content,
                "user_id": self.user_id}

    def __repr__(self):
        return f"Post('{self.title}', '{self.date_time}')"

class Comment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    date_time = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    content = db.Column(db.Text, nullable=False)
    post_id = db.Column(db.Integer, db.ForeignKey('post.id'), nullable=False)

    def serialize(self):
        return {"id": self.id,
                "date_time": self.date_time,
                "content": self.content,
                "post_id": self.post_id}

    def __repr__(self):
        return f"Comment('{self.content}', '{self.date_time}')"


class Followers(db.Model):
    __table_args__ = (db.UniqueConstraint('follow_id', 'followed_id'), )
    id = db.Column(db.Integer, primary_key=True)
    follow_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    followed_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    def __repr__(self):
        return f"Followers('{self.subject}', '{self.target}')"