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

@app.route('/class_add')
def class_add():
    return render_template('ClassAdd.html')           #查询成绩

@app.route('/student_regist')
def student_regist():
    return render_template('StudentRegist.html')        #注册学生

@app.route('/change_my_password')
def change_my_password():
    return render_template('ChangeMyPassword.html')     #更改老师密码

@app.route('/change_student_password')
def change_student_password():
    return render_template('ChangeStudentPassword.html')#更改学生密码

@app.route('/change_students_password')
def change_students_password():
    return render_template('ChangeStudentsPassword.html')#更改学生密码

@app.route('/change_data')
def change_data():
    return render_template('ChangeData.html')

@app.route('/student_data')
def student_data():
    return render_template('StudentData.html')           #查询学生资料

#学生登录
@app.route('/login')
def StudentLoginRequest():
    stu_id = int(request.args.get('id'))
    stu_passwd = str(request.args.get('password'))
    try:
        student = session.query(models.User).filter(models.User.power==0).filter(models.User.id==stu_id).first()
        if student.password == stu_passwd:
            posts = []
            posts.append(student)
            return render_template('student.html', posts=posts)
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

#学生课程录入
@app.route('/classadd')
def ClassAddRequest():
    cla_name = str(request.args.get('subject'))
    cla = session.query(models.Classes).filter(models.Classes.name == cla_name).first()
    if cla == None:
        classes = models.Classes(name = cla_name)
        session.add(classes)
        return '<h3>新添课程成功</h3>'
    else:
        return '<h3>新添课程已存在</h3>'

#学生成绩录入
@app.route('/scoreadd')
def ScoreAddRequest():
    stu_id = int(request.args.get('id'))
    stu_name = str(request.args.get('name'))
    cla_name = str(request.args.get('subject'))
    stu_score = int(request.args.get('fraction'))
    try:
        student = session.query(models.User).filter(models.User.power==0).filter(models.User.id==stu_id).first()
        if student.name == stu_name:
            cla = session.query(models.Classes).filter(models.Classes.name == cla_name).first()
            if cla == None:
                return '<h3>暂无此课</h3>'
            else:
                student.classes = [cla]
                session.commit()
                score = models.Scores(fraction = stu_score, user_id = stu_id, class_id = cla.id)
                session.add(score)
                session.commit()
                return '<h1>录入成功</h1>'
        else:
            return '<h1>学号与姓名不对等</h1>'
    except:
        return '<h1>学号有误</h1>'

#学生成绩删除
@app.route('/scoredelete')
def ScoreDeleteRquest():
    stu_id = int(request.args.get('id'))
    cla_name = str(request.args.get('subject'))
    stu_obj =session.query(models.User).filter_by(id = stu_id).first()
    score_obj =session.query(models.Scores).filter_by(user_id=stu_id).first()
    cla_obj = session.query(models.Classes).filter_by(name=cla_name).first()
    try:
        session.delete(score_obj) #删除分数
        stu_obj.classes.remove(cla_obj) #从一门课中删除一个学生
        session.commit()
        return '<h1>删除成功</h1>'
    except:
        return '<h1>删除出错</h1>'

#学生成绩查询
@app.route('/scorequery')
def ScoreQueryRquest():
    stu_id = int(request.args.get('id'))
    ret=(session.query(models.Scores,models.Classes).join(models.Classes,isouter=True)
            .filter(models.Scores.user_id==stu_id).all())
    length = len(ret) * 2
    i = 0
    dict_data = {}
    if i < length:
        for sco in ret:
            dict_data[i] = sco[1]                    #学生课程名称
            i = i + 1
            dict_data[i] = sco[0].fraction         #学生分数
            i = i + 1
    posts = []
    posts.append(dict_data)
    return render_template('ScoreQuery.html', posts=posts)


#修改老师密码
@app.route('/changemypassword')
def ChangeMyPasswordRequest():
    id = int(request.args.get('id'))
    oldpasswd = str(request.args.get('oldpasswd'))
    newpasswd1 = str(request.args.get('newpasswd1'))
    newpasswd2 = str(request.args.get('newpasswd2'))
    try:
        teacher = session.query(models.User).filter(models.User.power==1).filter(models.User.id==id).first()
        if teacher.password == oldpasswd:
            if newpasswd1 == newpasswd2:
                teacher.password = newpasswd1
                session.commit()
                return '<h1>密码修改成功</h1>'
            else:
                return '<h1>两次新密码不相同</h1>'
        else:
            return '<h1>密码错误</h1>'
    except:
        return '<h1>帐号不存在</h1>'

#老师修改学生密码
@app.route('/changestudentpassword')
def ChangeStudentPasswordRequest():
    id = int(request.args.get('id'))
    newpasswd = str(request.args.get('newpasswd'))
    try:
        stu = session.query(models.User).filter(models.User.power==0).filter(models.User.id==id).first()
        stu.password = newpasswd
        session.commit()
        return '<h1>密码修改成功</h1>'
    except:
        return '<h1>帐号不存在</h1>'

#学生修改学生密码
@app.route('/changestudentspassword')
def ChangeStudentsPasswordRequest():
    id = int(request.args.get('id'))
    oldpasswd = str(request.args.get('oldpasswd'))
    newpasswd1 = str(request.args.get('newpasswd1'))
    newpasswd2 = str(request.args.get('newpasswd2'))
    try:
        teacher = session.query(models.User).filter(models.User.power==0).filter(models.User.id==id).first()
        if teacher.password == oldpasswd:
            if newpasswd1 == newpasswd2:
                teacher.password = newpasswd1
                session.commit()
                return '<h1>密码修改成功</h1>'
            else:
                return '<h1>两次新密码不相同</h1>'
        else:
            return '<h1>密码错误</h1>'
    except:
        return '<h1>帐号不存在</h1>'

#学生资料更改
@app.route('/changedata')
def ChangeDataRequest():
    stu_id = int(request.args.get('id'))
    stu_birthday = int(request.args.get('birthday'))
    stu_collage = str(request.args.get('collage'))
    stu_major = str(request.args.get('major'))
    stu_grade = int(request.args.get('grade'))
    try:
        stu_obj =session.query(models.User).filter_by(id = stu_id).first()
        stu_obj.birthday = stu_birthday
        stu_obj.collage = stu_collage
        stu_obj.major = stu_major
        stu_obj.grade = stu_grade
        session.commit()
        return '<h3>学生信息更改成功</h3>'
    except:
        return '<h3>学生信息更改失败</h3>'


if __name__ == '__main__':
    app.run(debug=True)
