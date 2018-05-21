# -*- coding: UTF-8 -*-
from sqlalchemy import Table, Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

'''
import os
os.system("python /home/fty/flasky/app/drop_table.py")
'''
db_user = 'man_user'
passwd = '674099'
database = 'snailblog'

eng = "mysql+mysqldb://" + db_user + ":" + passwd + "@localhost:3306/" + database
engine = create_engine(eng, encoding='utf-8')

Base = declarative_base()

user_to_classes = Table('user_to_classes', Base.metadata,
                        Column('user_id',Integer,ForeignKey('user.id')),
                        Column('classes_id',Integer,ForeignKey('classes.id')),
                        )

class User(Base):
    __tablename__ = 'user'
    id = Column(Integer,primary_key=True)           #学号
    name = Column(String(10), nullable=False)       #姓名
    birthday = Column(Integer)                 #出生年月日
    collage = Column(String(20))                    #所属学院
    major = Column(String(20))                      #所属专业
    grade = Column(Integer)                    #年级
    password = Column(String(20), nullable=False)   #密码
    power = Column(Integer)                         #权限等级
    #建立虚拟关系关联其他表
    classes = relationship('Classes', secondary = user_to_classes, backref = 'myuser')

    def __repr__(self):
        return self.name 

class Classes(Base):
    __tablename__ = 'classes'
    id = Column(Integer,primary_key=True)
    name = Column(String(20), nullable=False)       #课程名

    def __repr__(self):
        return self.name 

class Scores(Base):
    __tablename__ = 'scores'
    id = Column(Integer,primary_key=True)
    fraction = Column(Integer, nullable=False) #分数
    #外键关联
    user_id = Column(Integer, ForeignKey("user.id"))
    class_id = Column(Integer, ForeignKey("classes.id"))
    classes = relationship('Classes', backref='classes_scores')
    user = relationship('User', backref = 'myscore')

    def __repr__(self):
        return "<学生学号:%s 课程代号:%s 分数:%s>" % (self.user_id, self.class_id, self.fraction) 

def init_db():
    Base.metadata.create_all(engine)

def drop_db():
    Base.metadata.drop_all(engine)

init_db()