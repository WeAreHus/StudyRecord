# -*- coding: utf-8 -*-
"""
from app import app
from .admin import admin
from .user import user
#这里分别给app注册了两个蓝图admin,user
#参数url_prefix='/xxx'的意思是设置request.url中的url前缀，
#即当request.url是以/admin或者/user的情况下才会通过注册的蓝图的视图方法处理请求并返回
app.register_blueprint(admin,url_prefix='/admin')
app.register_blueprint(user, url_prefix='/students')
"""
from datetime import datetime
from flask import render_template, session, redirect, url_for
from . import models

@app.route('/')
def login():
    return render_template('login.html')

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

# 老师登录
@app.route('/admin_login')
def admin_login():
    return render_template('AdminLogin.html') 

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


