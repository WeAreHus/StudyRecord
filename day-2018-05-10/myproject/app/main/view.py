# -*- coding: utf-8 -*-
from app import app
from .admin import admin
from .students import students
#这里分别给app注册了两个蓝图admin,user
#参数url_prefix='/xxx'的意思是设置request.url中的url前缀，
#即当request.url是以/admin或者/user的情况下才会通过注册的蓝图的视图方法处理请求并返回
app.register_blueprint(admin,url_prefix='/admin')
app.register_blueprint(user, url_prefix='/user')

#输入设定好的帐号密码进行登录操作,输入admin则进入管理员界面，否则进入学生界面
@app.route('/login', methods=['POST'])
def login():
    if request.form['username']=='admin' and request.form['password']=='password':
        return render_template('admin.html')
    return render_template('students.html')