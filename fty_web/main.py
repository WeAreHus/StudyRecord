# -*- coding: UTF-8 -*-
import pymysql
import MySQLdb
from flask import Flask
from flask import render_template
from flask import request   
import traceback

app = Flask(__name__)

administrator_name = 'admin'
administrator_passwd = 'admin'

@app.route('/')
def login():
    return render_template('login.html')

@app.route('/regist')
def regist():
    return render_template('regist.html')

@app.route('/insert')
def insert():
    return render_template('insert.html')

@app.route('/search')
def search():
    return render_template('search.html')

@app.route('/admin_login')
def admin_login():
    return render_template('admin_login.html')

@app.route('/changepasswd')
def changepasswd():
    return render_template('changepasswd.html')

#设置响应头
def Response_headers(content):    
    resp = Response(content)    
    resp.headers['Access-Control-Allow-Origin'] = '*'    
    return resp 

#数据库连接函数，传入姓名
def get_Table_Data(id, table):
    conn = MySQLdb.connect(
        host='127.0.0.1', port=3306,
        user='man_user', passwd='674099',
        db='snailblog', charset='utf8',
    )
    cur = conn.cursor()
    res = cur.execute("select * from "+ table +" where id = '" + id + "'")
    res = cur.fetchmany(res)
    cur.close()
    conn.commit()
    conn.close()
    return res

#获取注册请求及处理
@app.route('/registuser')
def getRigistRequest():
    db = pymysql.connect("localhost","man_user","674099","snailblog" )
    cursor = db.cursor()
    sql = ("INSERT INTO student(id, name, password) VALUES (" + 
           request.args.get('id') +
           "," +
           "'" + request.args.get('name') +  "'" +
           ", " + 
           "'"  + request.args.get('password') +   "'" +
           ")")
    try:
        cursor.execute(sql)
        db.commit()
        return '<h3>注册成功</h3>'
    except:
        traceback.print_exc()
        db.rollback()
        return '<h3>注册失败</h3>'
    db.close()

#主界面登录(学生端）
@app.route('/login')
def getLoginRequest():
    db = pymysql.connect("localhost","man_user","674099","snailblog" )
    cursor = db.cursor()
    sql = ("select * from student where id=" + request.args.get('id') + 
" and password="+"'" +request.args.get('password')+"'"+"")
    try:
        cursor.execute(sql)
        results = cursor.fetchall()
        print(len(results))
        if len(results)==1:
            id = request.args.get('id')
            data = get_Table_Data(id, 'student_grades')
            posts = []
            for value in data:
                dict_data = {}
                dict_data['id'] =  value[0]
                dict_data['name'] = value[1]
                dict_data['math'] = value[2]
                dict_data['Chinese'] = value[3]
                dict_data['English'] =  value[4]
                dict_data['physical'] =  value[5]
                dict_data['chemistry'] =  value[6]
                dict_data['biological'] =  value[7]
                dict_data['history'] =  value[8]
                dict_data['geography'] =  value[9]
                dict_data['political'] =  value[10]
                print value
                posts.append(dict_data)
            return render_template('student.html', posts=posts)
        else:
            return '<h3>用户名或密码不正确<h3>'
        db.commit()
    except:
        traceback.print_exc()
        db.rollback()
    db.close()

#管理员登录
@app.route('/adminlogin')
def getAdmin_loginRequest():
    name =  request.args.get('id')
    password =  request.args.get('password')
    if name == administrator_name and password == administrator_passwd:
        return render_template('administrator.html')
    else:
        return '<h3>用户名或密码不正确</h3>'

#成绩插入
@app.route('/grades_insert')
def grades_insert():
    id = request.args.get('id')
    name = request.args.get('name')
    data = get_Table_Data(id, 'student')
    key = 0
    for value in data:
        print str(id)
        print str(value[0])
        print str(name)
        print str(value[1])
        if str(id) == str(value[0]):
            key = 1
        else:
            return '<h3>录入失败:学号不正确</h3>'
        if str(name) == str(value[1]):
            key = 1
        else:
            return '<h3>录入失败:姓名不正确</h3>'
    if key == 1:
        db = pymysql.connect("localhost","man_user","674099","snailblog" )
        cursor = db.cursor()
        sql =( "INSERT INTO student_grades (id, name, math, Chinese, English, physical, chemistry, biological, history, geography, political) VALUES (" 
+ request.args.get('id') + "," + "'" + request.args.get('name') + "'" + "," + request.args.get('math') + "," + request.args.get('Chinese') + "," 
+ request.args.get('English') + "," + request.args.get('physical') + "," + request.args.get('chemistry') + "," + request.args.get('biological') + "," 
+ request.args.get('history') + "," + request.args.get('geography') + "," + request.args.get('political') + ")" )
        try:
            cursor.execute(sql)
            db.commit()
            return '<h3>录入成功</h3>' 
        except:
            traceback.print_exc()
            db.rollback()
            return '<h3>录入失败</h3>'
        db.close()

#成绩查询
@app.route('/grades_search', methods=['GET'])
def grades_search():
    #pdb.set_trace()
    id = request.args.get('id')
    data = get_Table_Data(id, 'student_grades')
    posts = []
    for value in data:
        dict_data = {}
        dict_data['id'] =  value[0]
        dict_data['name'] = value[1]
        dict_data['math'] = value[2]
        dict_data['Chinese'] = value[3]
        dict_data['English'] =  value[4]
        dict_data['physical'] =  value[5]
        dict_data['chemistry'] =  value[6]
        dict_data['biological'] =  value[7]
        dict_data['history'] =  value[8]
        dict_data['geography'] =  value[9]
        dict_data['political'] =  value[10]
        print value
        posts.append(dict_data)
    return render_template('student.html', posts=posts)

#更改密码
@app.route('/change_passwd')
def getchangepasswdRequest():
    pass

if __name__ == '__main__':
    app.run(debug=True)
