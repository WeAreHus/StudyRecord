# -*- coding: UTF-8 -*-
from sqlalchemy import Table, Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

#import os
#os.system("python /home/fty/flasky/app/drop_table.py")

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
        return "<user_id:%s object_id:%s fraction:%s>" % (self.user_id, self.class_id, str(self.fraction)) 

def init_db():
    Base.metadata.create_all(engine)

def drop_db():
    Base.metadata.drop_all(engine)

init_db()

'''
DBSession = sessionmaker(bind=engine)
session = DBSession()

user1 = User(name="fty", birthday=1999, collage ="jk",  major ="txgc", grade =1604, password ="674099", power =1)
user2 = User(name="cw", birthday=1998, collage ="jk",  major ="rjgc", grade =1607, password ="111111", power =1)
user3 = User(name="xjh", birthday=1998, collage ="jk",  major ="txgc", grade =1604, password ="123456", power =1)
c1 = Classes(name ="math")
c2 = Classes(name ="chinese")
c3 = Classes(name ="english")
s1 = Scores(fraction =99, user_id = 1, class_id = 1)
s2 = Scores(fraction =90, user_id = 2, class_id = 1)
s3 = Scores(fraction =80, user_id = 3, class_id = 1)
s4 = Scores(fraction =60, user_id = 1, class_id = 2)
s5 = Scores(fraction =94, user_id = 1, class_id = 3)

user1.classes = [c1, c3]
user2.classes = [c1, c2]
user3.classes = [c1, c2, c3]
session.add_all([user1, user2, user3, c1, c2, c3, s1, s2, s3, s4, s5])
session.commit()

#查询学生的课程
student = session.query(User).filter(User.name=="fty").first()
print(student.classes)
#查询课程的学生
object = session.query(Classes).filter(Classes.name=="math").first()
print(object.myuser)

#查询学生的成绩
student_score = session.query(User).filter(User.name=="fty").first()
print student_score.myscore
#查询math课的所有学生的成绩
class_score = session.query(Classes).filter(Classes.name=="math").first()
print class_score.classes_scores
#查询指定学生指定课程的分数(id为1的数学成绩)
ret=session.query(Scores,Classes).join(Classes,isouter=True).filter(Classes.name=='math').filter(Scores.user_id=='1').all()
print(ret)
session.close()

drop_db()
'''