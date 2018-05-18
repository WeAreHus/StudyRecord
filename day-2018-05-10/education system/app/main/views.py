# -*- coding: utf-8 -*-
from flask import Flask
from flask import render_template
from flask import request   
import traceback

#输入设定好的帐号密码进行登录操作,输入admin则进入管理员界面，否则进入学生界面
@app.route('/')
def login():
    return render_template('login.html')

@app.route('/regist')
def regist():
    return render_template('regist.html')

@app.route('/admin', methods=['GET'])
def admin():
    return render_template('admin.html')


#插入学生成绩
@app.route('/InsertGrades', methods=['GET'])
def Insertgrades():
    return render_template('Insertgrades.html')

@app.route('crxscj',methods=['POST'])
def crxscj():
        pass


#学生成绩修改
@app.route('/ChangeGrades', methods=['GET'] )
def ChangeGrades():
    return render_template('ChangeGrades.html')

@app.route('xgxscj'， methods=['POST'])
def xgxscj():
    pass


#学生成绩删除
@app.route('/DeleteGrades', methods=['GET'])
def DeleteGrades():
    return render_template('DeleteGrades.html')

@app.route('scxscj', methods=['POST'])
def scxscj():
    pass

#显示学生个人成绩信息页面，可输入学生姓名进行成个人信息查询
@app.route('/PersonalInformation', methods=['GET'])
def PersonalInformation():
    return render_template('Pinformation.html')

@app.route('/grxxcx', methods=['POST'])
def grxxcx():
    pass

#显示学生成绩查询页面，输入学生姓名即可进行成绩查询
@app.route('/selectgrades', methods=['GET'])
def selectgrades():
    return render_template('selectgrades.html')

@app.route('cjcx', methods=['POST'])
def cjcx():
    pass