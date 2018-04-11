# -*- encoding: utf-8 -*-
from flask import Flask, render_template, request
import MySQLdb
import traceback
import pdb

app = Flask(__name__)  # 创建一个wsgi应用
app.config.from_object(__name__)
#app.config.from_envvar('FLASK_SETTING',silent=True)


@app.route('/', methods=['GET','POST'])
def index():
    return render_template("login.html")

@app.route('/regist',methods=['GET'])
def request():
    return render_template("regist.html")


@app.route('/login',methods=['GET','POST'])
def getLoginRequest():
    #pdb.set_trace()
    db = MySQLdb.connect(host="localhost",user="cris",passwd="123456",db="Students",charset="utf8")
    #youbiao

    cur=db.cursor()
    pdb.set_trace()
    sql = "select * from class where username="+"'" +request.args.get('username')+  "'"+" and password="+"'" +request.args.get('password')+"'"+""
    try:
        # 执行sql语句
        cur.execute(sql)
        db.commit()
        results = cur.fetchall()
        print(len(results))
        if len(results)==1:
            return 'index.html'
        else:
            return '用户名或密码不正确'
        # 提交到数据库执行
        db.commit()
    except:
        # 如果发生错误则回滚
        traceback.print_exc()
        db.rollback()
    # 关闭数据库连接
    db.close()



@app.route('/register',methods=['GET'])
def  getRigistRequest():
    #pdb.set_trace()
    #连接数据库,此前在数据库中创建数据库TESTDB
    db = MySQLdb.connect(host="localhost",user="cris",passwd="123456",db="Students",charset="utf8")
    # 使用cursor()方法获取操作游标
    cur = db.cursor() 
    # SQL 插入语句
    sql = "INSERT INTO class (username,password) VALUES ('"+request.args.get('username')+"'"+", "+request.args.get('password')+")"
    try:
        cur.execute(sql)
        db.commit()
        return render_template("login.html")
    except:
        traceback.print_exc()
        db.rollback()
        return '注册失败'
    cursor.close()
    conn.close()

    	
"""@app.route('/login',methods=['POST'])
def suc(): 
    #pdb.set_trace()
    if request.form['username']=="admin" and request.form['password']=="123":
        return render_template("index.html")
    else:
        return ERROR"""

def get_table_data(name):
    db = MySQLdb.connect(host="localhost",user="cris",passwd="123456",db="Students",charset='utf8')
    cur=db.cursor()
  
    res=cur.execute("select * fron student where name = '" + name + "'")
    res=cur.fetchmany(res)
    cur.close()
    db.commit()
    db.close()
    return res

@app.route('/cjcx',methods=['GET'])
def chaxun():
    name = request.args.get('name')
    data =  get_Table_Data(name)
    posts=[]
    for value in data:
        dict_data = {}
        dict_data['id'] = value[0]
        dict_data['name'] = value[1]
    	dict_data['subject'] = value[2]
        dict_data['grades'] = value[3]
    	posts.append(dict_data)
    return render_template("grade.html",posts=posts)	
              
    
@app.route('/grade',methods=['GET'])
def getGrades():
    return render_template("grade.html")	   

if __name__ == '__main__':
    app.run()  # 启动app的调试模式


