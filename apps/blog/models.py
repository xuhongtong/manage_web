from datetime import datetime
from apps.ext import db


# 文章详情
class Article(db.Model):
    __tablename__ = 'article'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    tag1 = db.Column(db.String(100), nullable=True)
    tag2 = db.Column(db.String(100), nullable=True)
    tag3 = db.Column(db.String(100), nullable=True)
    short_content = db.Column(db.String(512), nullable=True)
    content = db.Column(db.Text, nullable=False)
    update_time = db.Column(db.DateTime, default=datetime.now)
    create_time = db.Column(db.DateTime, default=datetime.now())
    author_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    category_id = db.Column(db.Integer, db.ForeignKey('category.id'))
    user = db.relationship('User', backref=db.backref('articles'))  # 正向与反向引用
    category = db.relationship('Category', backref=db.backref('articles'))  # 正向与反向引用
    is_delete = db.Column(db.Boolean, default=0)


class Category(db.Model):
    __tablename__ = 'category'
    id = db.Column(db.Integer, primary_key=True)
    category = db.Column(db.String(100), nullable=True)
    update_time = db.Column(db.DateTime, default=datetime.now)
    create_time = db.Column(db.DateTime, default=datetime.now())
    is_delete = db.Column(db.Boolean, default=0)


class Notice(db.Model):
    __tablename__ = 'notice'
    id = db.Column(db.Integer, primary_key=True)
    message = db.Column(db.String(512), nullable=True)
    update_time = db.Column(db.DateTime, default=datetime.now)
    create_time = db.Column(db.DateTime, default=datetime.now())
    is_delete = db.Column(db.Boolean, default=0)