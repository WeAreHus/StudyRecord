# -*- coding: utf-8 -*-
from flask import Blueprint,render_template, request

admin = Blueprint('admin',__name__)

#学生用户注册
@admin.route('/student_regist')
def student_regist():
    return render_template('StudentRegist.html')   

@admin.route('/studentregist')
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
        

#录入学生成绩
@admin.route('/InsertGrades', methods=['GET'])
def Insertgrades():
    return render_template('Insertgrades.html')

@admin.route('crxscj',methods=['POST'])
def crxscj():
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


#学生成绩修改
@admin.route('/ChangeGrades', methods=['GET'] )
def ChangeGrades():
    return render_template('ChangeGrades.html')

@admin.route('xgxscj'， methods=['POST'])
def xgxscj():
    pass


#学生成绩删除
@admin.route('/DeleteGrades', methods=['GET'])
def DeleteGrades():
    return render_template('DeleteGrades.html')

@admin.route('scxscj', methods=['POST'])
def scxscj():
    pass
