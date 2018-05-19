# -*- coding: UTF-8 -*-
import models

from flask import Flask
from flask import render_template
from flask import request   
import traceback

from sqlalchemy.orm import sessionmaker

Session_class = sessionmaker(bind=models.engine)
session = Session_class()

app = Flask(__name__)

@app.route('/')
def login():
    return render_template('login.html')

@app.route('/admin_login')
def admin_login():
    return render_template('AdminLogin.html')           #老师登录

@app.route('/score_add')
def score_add():
    return render_template('SacoreAdd.html')            #添加成绩

@app.route('/score_delete')
def score_delete():
    return render_template('ScoreDelete.html')          #删除成绩

@app.route('/score_query')
def score_query():
    return render_template('ScoreQuery.html')           #查询成绩

@app.route('/student_regist')
def student_regist():
    return render_template('StudentRegist.html')        #注册学生

@app.route('/change_my_password')
def change_my_password():
    return render_template('ChangeMyPassword.html')     #更改老师密码

@app.route('/change_student_password')
def change_student_password():
    return render_template('ChangeStudentPassword.html')#更改学生密码

#学生登录
@app.route('/login')
def StudentLoginRequest():
    stu_id = int(request.args.get('id'))
    stu_passwd = str(request.args.get('password'))
    try:
        student = session.query(models.User).filter(models.User.power==0).filter(models.User.id==stu_id).first()
        if student.password == stu_passwd:
            return render_template('student.html')
        else:
            return '<h1>密码错误</h1>'
    except:
        return '<h1>账户名错误</h1>'

#教师登录
@app.route('/adminlogin')
def AdminLoginRequest():
    ad_id = int(request.args.get('id'))
    ad_passwd = str(request.args.get('password'))
    try:
        admin = session.query(models.User).filter(models.User.power==1).filter(models.User.id==ad_id).first()
        if admin.password == ad_passwd:
            return render_template('admin.html')
        else:
            return '<h1>密码错误</h1>'
    except:
        return '<h1>账户名错误</h1>'

#学生用户注册
@app.route('/studentregist')
def StudentRegistRequest():
    stu_id = int(request.args.get('id'))
    stu_passwd = str(request.args.get('password'))
    stu_name = str(request.args.get('name'))
    stu_birthday = int(request.args.get('birthday'))
    stu_collage = str(request.args.get('collage'))
    stu_major = str(request.args.get('major'))
    stu_grade = int(request.args.get('grade'))
    stu_power = 0
    try:
        student = models.User(id = stu_id, password = stu_passwd, 
                            name = stu_name, birthday = stu_birthday, 
                            collage = stu_collage, major = stu_major, 
                            grade = stu_grade, power = stu_power)
        session.add(student)
        session.commit()
        return '<h3>学生注册成功</h3>'
    except:
        return '<h3>学生注册失败</h3>'

#学生成绩录入
@app.route('/scoreadd')
def ScoreAddRequest():
    stu_id = int(request.args.get('id'))
    stu_name = str(request.args.get('name'))
    cla_name = str(request.args.get('object'))
    stu_score = int(request.args.get('fraction'))
    try:
        student = session.query(models.User).filter(models.User.power==0).filter(models.User.id==stu_id).first()
        if student.name == stu_name:
            cla = models.Classes(name = cla_name)
            student.classes = [cla]
            session.add(cla)
            session.commit()
            subject = session.query(models.Classes).filter(models.Classes.name == cla_name).first()
            score = models.Scores(fraction = stu_score, user_id = stu_id, class_id = subject.id)
            session.add(score)
            session.commit()
            return '<h1>录入成功</h1>'
        else:
            return '<h1>学号与姓名不对等</h1>'
    except:
        return'<h1>学号有误</h1>'

#学生成绩删除
@app.route('/scoredelete')
def ScoreDeleteRquest():
    stu_id = int(request.args.get('id'))
    stu_name = str(request.args.get('name'))
    cla_name = str(request.args.get('subject'))
    

if __name__ == '__main__':
    app.run(debug=True)