# -*- encoding: utf-8 -*-
from flask import Flask, render_template, request

#username="admin"
#password="123"
app = Flask(__name__)  # 创建一个wsgi应用
app.config.from_object(__name__)
app.config.from_envvar('FLASK_SETTING',silent=True)

@app.route('/',methods=['GET','POST'])  # 添加路由：根
def index():
    return render_template("login.html")  # 输出一个字符串


@app.route('/login', methods=['POST'])
def suc():
    if request.form['username']=="admin" and request.form['password']=="123":
        return render_template('success.html')
    else:
        return '错误！'


if __name__ == '__main__':
    app.run()  # 启动app的调试模式

