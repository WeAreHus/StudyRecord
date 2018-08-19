# -*- coding: UTF-8 -*-
import datetime

from flask import Flask
from flask import render_template
from flask import request   
import traceback

from sqlalchemy.orm import sessionmaker

import models

Session_class = sessionmaker(bind=models.engine)

app = Flask(__name__)

log_id = 0

@app.route('/')
def login():
    return render_template('login.html')

#老师登录
@app.route('/admin_login')
def admin_login():
    return render_template('AdminLogin.html')

#添加成绩
@app.route('/score_add')
def score_add():
    return render_template('ScoreAdd.html')

#删除成绩
@app.route('/score_delete')
def score_delete():
    return render_template('ScoreDelete.html')

#老师查询成绩
@app.route('/score_query')
def score_query():
    return render_template('ScoreQuery.html')

#学生查询成绩
@app.route('/student_score_query')
def student_score_query():
    return render_template('StudentScoreQuery.html')

#添加课程
@app.route('/class_add')
def class_add():
    return render_template('ClassAdd.html')

#注册学生
@app.route('/student_regist')
def student_regist():
    return render_template('StudentRegist.html')

#更改老师密码
@app.route('/change_my_password')
def change_my_password():
    return render_template('ChangeMyPassword.html')

#老师更改学生密码
@app.route('/change_student_password')
def change_student_password():
    return render_template('ChangeStudentPassword.html')

#学生查询个人资料
@app.route('/student_data')
def students_data():
    return render_template('StudentData.html')

#学生更改学生密码
@app.route('/change_students_password')
def change_students_password():
    return render_template('ChangeStudentsPassword.html')

#更改学生信息
@app.route('/change_data')
def change_data():
    return render_template('ChangeData.html')

#查询学生资料
@app.route('/student_data')
def student_data():
    return render_template('StudentData.html')

#分界线

#学生登录
@app.route('/login')
def StudentLoginRequest():
    #获取当前时间
    time = datetime.datetime.now().strftime('%H')
    now_time = int(time)
    if now_time >= 5 and now_time <11 :
        time = "Good morning"
    elif now_time >= 11 and now_time <18 :
        time = "Good afternoon"
    else:
        time = "Good evening"
    session = Session_class()
    global log_id
    stu_id = int(request.args.get('id'))
    log_id = stu_id
    stu_passwd = str(request.args.get('password'))
    try:
        student = session.query(models.User).filter(models.User.power==0).filter(models.User.id==stu_id).first()
        if student.password == stu_passwd:
            posts = []
            posts.append(student.name)
            posts.append(time)
            session.close()
            return render_template('student.html',posts = posts)
        else:
            return render_template('login.html', error='PASSWORD ERROR')
    except:
        return render_template('login.html', error='ID ERROR')

#教师登录
@app.route('/adminlogin')
def AdminLoginRequest():
    session = Session_class()
    ad_id = int(request.args.get('id'))
    ad_passwd = str(request.args.get('password'))
    try:
        admin = session.query(models.User).filter(models.User.power==1).filter(models.User.id==ad_id).first()
        if admin.password == ad_passwd:
            session.close()
            return render_template('admin.html')
        else:
            return render_template('AdminLogin.html', error='PASSWORD ERROR')
    except:
        return render_template('AdminLogin.html', error='ID ERROR')

#学生用户注册
@app.route('/studentregist')
def StudentRegistRequest():
    session = Session_class()
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
        return render_template('StudentRegist.html', error='REGIST SUCCESS')
    except:
        return render_template('StudentRegist.html', error='REGIST ERROR')

#学生课程录入
@app.route('/classadd')
def ClassAddRequest():
    session = Session_class()
    cla_name = str(request.args.get('subject'))
    cla = session.query(models.Classes).filter(models.Classes.name == cla_name).first()
    if cla == None:
        classes = models.Classes(name = cla_name)
        session.add(classes)
        session.commit()
        session.close()
        return render_template('ClassAdd.html', error = 'New class adding success')
    else:
        return render_template('ClassAdd.html', error = 'The class already exists')

#学生成绩录入
@app.route('/scoreadd')
def ScoreAddRequest():
    session = Session_class()
    stu_id = int(request.args.get('id'))
    stu_name = str(request.args.get('name'))
    cla_name = str(request.args.get('subject'))
    stu_score = int(request.args.get('fraction'))
    try:
        student = session.query(models.User).filter(models.User.power==0).filter(models.User.id==stu_id).first()
        i = 0
        for scla in student.classes:
            if str(scla) == cla_name:
                i = 1
        if i == 1 :
            return render_template('ScoreAdd.html', error = 'The student already got the score')
        else:
            student = session.query(models.User).filter(models.User.power==0).filter(models.User.id==stu_id).first()
            if student.name == stu_name:
                cla = session.query(models.Classes).filter(models.Classes.name == cla_name).first()
                if cla == None:
                    return render_template('ScoreAdd.html', error = 'There is no such class')
                else:
                    student.classes.append(cla)
                    session.commit()
                    score = models.Scores(fraction = stu_score, user_id = stu_id, class_id = cla.id)
                    session.add(score)
                    session.commit()
                    session.close()
                    return render_template('ScoreAdd.html', error = 'The score add success')
            else:
                return render_template('ScoreAdd.html', error = 'id or name error')
    except:
        return render_template('ScoreAdd.html', error = 'ID ERROR')

#学生成绩删除
@app.route('/scoredelete')
def ScoreDeleteRquest():
    session = Session_class()
    stu_id = int(request.args.get('id'))
    cla_name = str(request.args.get('subject'))
    stu_obj =session.query(models.User).filter_by(id = stu_id).first()
    score_obj =session.query(models.Scores).filter_by(user_id=stu_id).first()
    cla_obj = session.query(models.Classes).filter_by(name=cla_name).first()
    try:
        session.delete(score_obj) #删除分数
        stu_obj.classes.remove(cla_obj) #从一门课中删除一个学生
        session.commit()
        session.close()
        return render_template('ScoreDelete.html', error = 'DELETE SUCCESS')
    except:
        return render_template('ScoreDelete.html', error = 'DELETE ERROR')

#老师查询学生成绩
@app.route('/scorequery')
def ScoreQueryRquest():
    session = Session_class()
    stu_id = int(request.args.get('id'))
    try:
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
        session.close()
        return render_template('ScoreQuery.html', posts=posts)
    except:
        return render_template('ScoreQuery.html', error='ID ERROR')

#学生查询自己成绩
@app.route('/studentscorequery')
def StudentScoreQueryRquest():
    session = Session_class()
    ret=(session.query(models.Scores,models.Classes).join(models.Classes,isouter=True)
            .filter(models.Scores.user_id==log_id).all())
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
    session.close()
    return render_template('StudentScoreQuery.html', posts=posts)

#修改老师密码
@app.route('/changemypassword')
def ChangeMyPasswordRequest():
    session = Session_class()
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
                session.close()
                return render_template('ChangeMyPassword.html', error='Password reset complete')
            else:
                return render_template('ChangeMyPassword.html', error='New passwords are not the same')
        else:
            return render_template('ChangeMyPassword.html', error='Password error')
    except:
        return render_template('ChangeMyPassword.html', error='ID ERROR')

#老师修改学生密码
@app.route('/changestudentpassword')
def ChangeStudentPasswordRequest():
    session = Session_class()
    id = int(request.args.get('id'))
    newpasswd = str(request.args.get('newpasswd'))
    try:
        stu = session.query(models.User).filter(models.User.power==0).filter(models.User.id==id).first()
        stu.password = newpasswd
        session.commit()
        session.close()
        return render_template('ChangeStudentPassword.html', error='Password reset complete')
    except:
        return render_template('ChangeStudentPassword.html', error='ID ERROR')

#学生个人资料查询
@app.route('/studentdata')
def StudentDataRequest():
    session = Session_class()
    print log_id
    try:
        student = session.query(models.User).filter(models.User.power==0).filter(models.User.id==log_id).first()
        posts = []
        posts.append(student)
        session.close()
        return render_template('StudentData.html', posts=posts)
    except:
        return render_template('StudentData.html', error='ERROR!')

#学生修改学生密码
@app.route('/changestudentspassword')
def ChangeStudentsPasswordRequest():
    session = Session_class()
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
                session.close()
                return render_template('ChangeStudentsPassword.html', error='Password reset complete')
            else:
                return render_template('ChangeStudentsPassword.html', error='New passwords are not the same')
        else:
            return render_template('ChangeStudentsPassword.html', error='PASSWORD ERROR')
    except:
        return render_template('ChangeStudentsPassword.html', error='ID ERROR')

#学生资料更改
@app.route('/changedata')
def ChangeDataRequest():
    session = Session_class()
    stu_birthday = int(request.args.get('birthday'))
    stu_collage = str(request.args.get('collage'))
    stu_major = str(request.args.get('major'))
    stu_grade = int(request.args.get('grade'))
    try:
        stu_obj =session.query(models.User).filter_by(id = log_id).first()
        stu_obj.birthday = stu_birthday
        stu_obj.collage = stu_collage
        stu_obj.major = stu_major
        stu_obj.grade = stu_grade
        session.commit()
        session.close()
        return render_template('ChangeData.html', error='reset success')
    except:
        return render_template('ChangeData.html', error='reset error')

if __name__ == '__main__':
    app.run(debug=True)