# -*- coding: UTF-8 -*-
import MySQLdb
from flask import Flask
from flask import render_template
from flask import request   
import traceback  

app = Flask(__name__)

#默认路径访问登录页面
@app.route('/')
def login():
    return render_template('login.html')

#默认路径访问注册页面
@app.route('/regist')
def regist():
    return render_template('regist.html')

@app.route('/grade')
def getGrades():
    return render_template("grade.html")

#获取登录参数及处理
@app.route('/login')
def getLoginRequest():
<<<<<<< HEAD
    #pdb.set_trace()
    db = MySQLdb.connect(host="localhost",user="root",passwd="xx1997",db="grades",charset="utf8")
    #youbiao

    cur=db.cursor()
    pdb.set_trace()
    sql = "select * from class where name = "+"'"+request.args.get('username')+ "'"+" and password="+"'" +request.args.get('password')+"'"+""
=======
    db =MySQLdb.connect(
        host='localhost', port=3306,
        user='man_user', passwd='674099',
        db='snailblog', charset='utf8',
    )
    cursor = db.cursor()
    sql = ("select * from class where username=" + "'" + request.args.get('username') + "'" +
            " and password=" + "'" + request.args.get('password') + "'" + "")
>>>>>>> 4b75ab60e3292a0ef685b0276be9f355cfa3ca0d
    try:
        cursor.execute(sql)
        results = cursor.fetchall()
        print(len(results)) 
        if len(results)==1:
            return render_template('index.html')
        else:
            return '用户名或密码不正确'
        db.commit()
    except:
        traceback.print_exc()
        db.rollback()
    db.close()

<<<<<<< HEAD


@app.route('/register',methods=['GET'])
def  getRigistRequest():
    #pdb.set_trace()
    #连接数据库,此前在数据库中创建数据库TESTDB
    db = MySQLdb.connect(host="localhost",user="root",passwd="xx1997",db="grades",charset="utf8")
    # 使用cursor()方法获取操作游标
    cur = db.cursor() 
    # SQL 插入语句
    sql = "INSERT INTO class (username,password) VALUES ('"+request.args.get('username')+"'"+", "+request.args.get('password')+")"
=======
#获取注册请求及处理
@app.route('/register')
def getRigistRequest():
    db =MySQLdb.connect(
        host='localhost', port=3306,
        user='man_user', passwd='674099',
        db='snailblog', charset='utf8',
    ) 
    cursor = db.cursor()
    sql = ( "INSERT INTO class (username,password) VALUES ('" +
            request.args.get('username') + "'" +
            ", " + request.args.get('password') + ")" )
>>>>>>> 4b75ab60e3292a0ef685b0276be9f355cfa3ca0d
    try:
        cursor.execute(sql)
        db.commit()
        return render_template('login.html') 
    except:
        traceback.print_exc()
        db.rollback()
        return '注册失败'
    db.close()
    	
"""@app.route('/login',methods=['POST'])
def suc(): 
    #pdb.set_trace()
    if request.form['username']=="admin" and request.form['password']=="123":
        return render_template("index.html")
    else:
        return ERROR"""

def get_table_data(name):
    db =MySQLdb.connect(
        host='127.0.0.1', port=3306,
        user='man_user', passwd='674099',
        db='snailblog', charset='utf8',
    )
    cur=db.cursor()
<<<<<<< HEAD
  
    res=cur.execute("select * from student where name = '" + name + "'")
=======
    res=cur.execute("select * from students where name = '" + name + "'")
>>>>>>> 4b75ab60e3292a0ef685b0276be9f355cfa3ca0d
    res=cur.fetchmany(res)
    cur.close()
    db.commit()
    db.close()
    return res

@app.route('/cjcx',methods=['GET'])
def chaxun():
    name = request.args.get('username')
    print type(name)
    name = str(name)
    print type(name)

    data =  get_table_data(name)
    posts=[]
    for value in data:
        dict_data = {}
        dict_data['id'] = value[0]
        dict_data['name'] = value[1]
    	dict_data['subject'] = value[2]
        dict_data['grades'] = value[3]
    	posts.append(dict_data)
    return render_template("grade.html",posts=posts)	
              


if __name__ == '__main__':
    app.run(debug=True)  # 启动app的调试模式


