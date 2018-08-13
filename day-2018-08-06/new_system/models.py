# -*- coding: UTF-8 -*-
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy(use_native_unicode='utf8')

#学生表
class User(db.Model):
    __tablename__ = 'user'
    id = db.Column(db.BIGINT,primary_key=True)                                               #学号
    password = db.Column(db.String(100), nullable=False)                                      #密码
    name = db.Column(db.String(10), nullable=False)
    score_path = db.Column(db.String(100))

    def __init__(self, id, password, name, score_path):
        self.id = id
        self.password = password
        self.name = name
        self.score_path = score_path