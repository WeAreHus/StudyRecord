# -*- coding: utf-8 -*-
from flask import Flask
from flask import request
from flask import render_template
import MySQLdb
import pdb

app = Flask(__name__)

#数据库连接函数，传入姓名
def get_Table_Data(name):
    conn = MySQLdb.connect(
        host='127.0.0.1', port=3306,
        user='root', passwd='xx1997',
        db='grades', charset='utf8',
    )
    cur = conn.cursor()
    res = cur.execute("select * from students where name = '" + name + "'")
    res = cur.fetchmany(res)
    cur.close()
    conn.commit()
    conn.close()
    return res
 

#登录界面
@app.route('/', methods=['GET', 'POST'])
def home():
    return render_template('login.html')

#输入设定好的帐号密码进行登录操作,输入admin则进入管理员界面，否则进入学生界面
@app.route('/login', methods=['POST'])
def login():
    if request.form['username']=='admin' and request.form['password']=='password':
        return render_template('admin.html')
    return render_template('students.html')

#显示学生用户的界面
@app.route('/students', methods=['GET'])
def selectgrades():
    return render_template('students.html')

#显示管理员界面
"""@app.route('/admin', methods=['GET'])
    return render_template('admin.html')"""

#插入学生成绩的界面
@app.route('/crxscj', methods=['GET'])
def crxscj(): 
    return render_template('crxscj.html')

#获取表单数据并插入数据库中
@app.route('/crcj', methods=['POST'] )
def crcj():
    pdb.set_trace()
    id = request.form.get('userid')
    name = request.form.get('username')
    subject = request.form.get('usersubject')
    grade = request.form.get('usergrade')
    conn = MySQLdb.connect(
        host='127.0.0.1', port=3306,
        user='root', passwd='xx1997',
        db='grades', charset='utf8',
    )
    cur = conn.cursor()
    sql = "insert into students (id, name, subject, grade) values ('"+id+"','"+ name+"','"+ subject+"','"+ grade+"')"
    cur.execute(sql)
    cur.close()
    conn.commit()
    conn.close()
    return "插入成功"

#学生进行自主查询成绩界面
@app.route('/cjcx', methods=['GET'])
def cjcx():
    #pdb.set_trace()
    name = request.args.get('username')
    data = get_Table_Data(name)
    posts = []
    for value in data:
        dict_data = {}
        dict_data['id'] =  value[0]
        dict_data['name'] = value[1]
        dict_data['subject'] = value[2]
        dict_data['grade'] = value[3]
        posts.append(dict_data)
    return render_template('grades_index.html', posts=posts)

if __name__ == '__main__':
    app.run()
