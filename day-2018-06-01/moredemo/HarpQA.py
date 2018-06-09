#coding:utf8
from flask import Flask, render_template, request, flash, session, url_for, redirect, g
from models import db, Users, Questions, Comments
from werkzeug.security import generate_password_hash
from sqlalchemy import or_
from os import path
from werkzeug import secure_filename

from exts import validate, validate_func, allowed_file
import config

app = Flask(__name__)
app.config.from_object(config)
db.init_app(app)


#上下文管理器
@app.context_processor
def my_context_processor():
    if hasattr(g, 'user'):
        return {'login_user': g.user.username}
    return {}

#钩子函数，得到当期登录用户的User对象
@app.before_request
def my_before_request():
    username = session.get('username')
    if username:
        g.user = Users.query.filter(Users.username == username).first()

@app.route('/')
def home():
    questions = Questions.query.order_by(Questions.create_time.desc()).all()
    return render_template('home.html', questions=questions)

#注册
@app.route('/register/', methods=['GET', 'POST'])
def register():
    if request.method == 'GET':
        return render_template('register.html')
    else:
        username = request.form.get('username')
        password1 = request.form.get('password1')
        password2 = request.form.get('password2')
        #返回操作结果指示
        message = validate(username, password1, password2)
        flash(message)
        if 'successful' in message:
            #新建Users表对象，密码加密
            new_user = Users(username=username, password=generate_password_hash(password1))
            db.session.add(new_user)
            db.session.commit()
            session['status'] = 'OK'
            return redirect(url_for('login'))
        else:
            session['status'] = 'BAD'
            return render_template('register.html')

#登录
@app.route('/login/', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        return render_template('login.html')
    else:
        username = request.form.get('username')
        password = request.form.get('password1')
        #返回操作结果指示
        message = validate(username, password)
        if 'successful' in message:
            session['username'] = username
            session.permanent = True
            session['status'] = 'OK'
            return redirect(url_for('home'))
        else:
            flash(message)
            session['status'] = 'BAD'
            return render_template('login.html')

#注销
@app.route('/logout/')
def logout():
    session.clear()
    return redirect(url_for('home'))

#发布问答
@app.route('/question/', methods=['GET', 'POST'])
def question():
    if request.method == 'GET':
        return render_template('question.html')
    else:
        if hasattr(g, 'user'):
            question_title = request.form.get('question_title').strip()
            question_desc = request.form.get('question_desc').strip()
            author_id = g.user.id
            new_question = Questions(title=question_title, content=question_desc, author_id=author_id)
            db.session.add(new_question)
            db.session.commit()
            return redirect(url_for('home'))
        else:
            flash('Please log in first')
            return redirect(url_for('login'))

#url传参，评论功能
@app.route('/details/<question_id>/', methods=['GET', 'POST'])
def details(question_id):
    if request.method == 'GET':
        question_obj = Questions.query.filter(Questions.id == question_id).first()
        return render_template('details.html', question=question_obj)
    else:
        if hasattr(g, 'user'):
            content = request.form.get('comment_desc')
            author_id = g.user.id
            comment = Comments(content=content, question_id=question_id, author_id=author_id)
            db.session.add(comment)
            db.session.commit()
            return redirect(url_for('details', question_id=question_id))
        else:
            flash('Please log in first')
            return redirect(url_for('login'))

#导航栏中的搜索功能
@app.route('/search')
def search():
    # 获取GET数据，注意和获取POST数据的区别
    keyword = request.args.get('keyword')
    result = Questions.query.filter(or_(Questions.title.contains(keyword),
                                    Questions.content.contains(keyword))).order_by(
                                    Questions.create_time.desc()).all()
    if result:
        return render_template('home.html', questions=result, search_title=True)
    else:
        return render_template('warn.html')

#用户中心
@app.route('/user/', methods=['GET', 'POST'])
def user_center():
    return render_template('user.html', user=g.user)

#修改密码
@app.route('/user/security/', methods=['GET', 'POST'])
def security():
    if request.method == 'GET':
        return render_template('security.html')
    else:
        o_password = request.form.get('o_password')
        password1 = request.form.get('password1')
        password2 = request.form.get('password2')
        message = validate_func(g.user, o_password, password1, password2)   
        if 'successful' in message:
            g.user.password = generate_password_hash(password1)
            db.session.commit()
            session.clear()
            flash(message)
            return redirect(url_for('logout'))
        else:
            flash(message)
            session['status'] = 'BAD'
            return render_template('security.html')

#上传头像
@app.route('/user/avatar/', methods=['GET', 'POST'])
def avatar():
    if request.method == 'POST':
        file = request.files['avatar_upload']
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            base_path = path.abspath(path.dirname(__file__))
            filename = str(g.user.id) + '.' + filename.rsplit('.', 1)[1]
            file_path = path.join(base_path, 'static', 'images', 'uploads', filename)
            file.save(file_path)
            g.user.avatar_path = 'images/uploads/' + filename
            db.session.commit()
    return render_template('avatar.html', user=g.user)

if __name__ == '__main__':
    app.run()