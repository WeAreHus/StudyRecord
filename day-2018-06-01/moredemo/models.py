#coding:utf8
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()

class Users(db.Model):
    __tablename__ = 'users_info'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(32), nullable=False)
    password = db.Column(db.String(100), nullable=False)
    # 用户建立时间
    register_time = db.Column(db.DateTime, nullable=False, default=datetime.now())
    # 头像目录
    avatar_path = db.Column(db.String(256), nullable=False, default='images/doraemon.jpg')
    
class Questions(db.Model):
    __tablename__ = 'questions_info'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    # 标题
    title = db.Column(db.String(100), nullable=False)
    # 内容
    content = db.Column(db.TEXT, nullable=False)
    # 作者id
    author_id = db.Column(db.Integer, db.ForeignKey('users_info.id'))
    # 问题提出的时间
    create_time = db.Column(db.DateTime, nullable=False, default=datetime.now())

    author = db.relationship('Users', backref=db.backref('questions', order_by=create_time.desc()))

class Comments(db.Model):
    __tablename__ = 'comments_info'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    # 评论的内容
    content = db.Column(db.TEXT, nullable=False)
    # 评论对应的问题的id
    question_id = db.Column(db.Integer, db.ForeignKey('questions_info.id'))
    # 发出评论的作者id
    author_id = db.Column(db.Integer, db.ForeignKey('users_info.id'))
    # 评论时间
    create_time = db.Column(db.DateTime, nullable=False, default=datetime.now())

    author = db.relationship('Users', backref=db.backref('comments'))
    question = db.relationship('Questions', backref=db.backref('comments', order_by=create_time.desc()))