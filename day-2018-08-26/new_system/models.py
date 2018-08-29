# -*- coding: UTF-8 -*-
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy(use_native_unicode='utf8')


# 学生与课程的多对多关系表
stu_with_sub = db.Table('stu_with_sub',
                        db.Column('student_id', db.BIGINT, db.ForeignKey(
                            'student_information.id'), primary_key=True),
                        db.Column('subject_id', db.Integer, db.ForeignKey(
                            'subject_information.id'), primary_key=True),
                        )

# 学生表
class Student(db.Model):
    __tablename__ = 'student_information'
    id = db.Column(db.BIGINT, primary_key=True)
    name = db.Column(db.String(10), nullable=False)
    # 建立与课程表的虚拟关系，实现查课程下的学生
    subject = db.relationship(
        'Subject', secondary=stu_with_sub, backref=db.backref('student'))

    def __init__(self, id, name):
        self.id = id
        self.name = name


class Subject(db.Model):
    __tablename__ = 'subject_information'
    id = db.Column(db.Integer, primary_key=True)
    school_year = db.Column(db.String(10), nullable=False)  # 学年
    school_term = db.Column(db.Integer, nullable=False)  # 学期
    class_code = db.Column(db.String(20), nullable=False)  # 课程代码
    class_name = db.Column(db.String(20), nullable=False)  # 课程名称
    class_category = db.Column(db.String(10), nullable=False)  # 课程性质
    credit = db.Column(db.Integer, nullable=False)  # 学分
    class_ownership = db.Column(db.String(10))  # 课程归属
    minor_tab = db.Column(db.Integer)  # 辅修标记
    collage = db.Column(db.String(20))  # 学院名称
    resit_tab = db.Column(db.Integer)  # 重修标记
    class_English_name = db.Column(db.String(50))  # 课程英文名称

    def __init__(self, school_year, school_term, class_code, class_name, class_category, credit,
                 class_ownership=None, minor_tab=None, collage=None, resit_tab=None, class_English_name=None):
        self.school_year = school_year
        self.school_term = school_term
        self.class_code = class_code
        self.class_name = class_name
        self.class_category = class_category
        self.credit = credit
        self.class_ownership = class_ownership
        self.minor_tab = minor_tab
        self.collage = collage
        self.resit_tab = resit_tab
        self.class_English_name = class_English_name


class Score(db.Model):
    __tablename__ = 'score_information'
    id = db.Column(db.Integer, primary_key=True)
    score = db.Column(db.Integer, nullable=False)  # 成绩
    GPA = db.Column(db.Float, nullable=False)  # 绩点
    resit_score = db.Column(db.Integer)  # 补考成绩
    restudy_score = db.Column(db.Integer)  # 重修成绩
    note = db.Column(db.String(50))  # 备注

    # 查指定课程下所有学生的成绩
    subject_id = db.Column(db.Integer, db.ForeignKey("subject_information.id"))
    subject = db.relationship('Subject', backref=db.backref('score'))

    # 查指定学生的所有成绩
    student_id = db.Column(db.BIGINT, db.ForeignKey("student_information.id"))
    student = db.relationship('Student', backref=db.backref('score'))

    def __init__(self, score, GPA, subject_id, student_id, resit_score=None, restudy_score=None, note=None):
        self.score = score
        self.GPA = GPA
        self.subject_id = subject_id
        self.student_id = student_id
        self.resit_score = resit_score
        self.restudy_score = restudy_score
        self.note = note