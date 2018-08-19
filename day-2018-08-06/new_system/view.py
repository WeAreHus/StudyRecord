#coding:utf8
from flask import (Flask, g, redirect, render_template, request, session,
                   url_for)

import config
from models import User, db
from spider import spider_login, getgrades, parser
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
app.config.from_object(config)
db.init_app(app)

with app.test_request_context():
    #db.drop_all()
    db.create_all()

@app.context_processor
def my_context_processor():
    if hasattr(g, 'user'):
        return {'login_user': g.user}
    return {}

@app.before_request
def my_before_request():
    id = session.get('id')
    user = session.get('user')
    name = session.get('name')
    if id:
        if user == 'student':
            g.user = name
        elif user == 'teacher':
            g.user = User.query.filter(User.id == id).first()

@app.route('/')
def login():
    user = 1
    return render_template('login.html', user=user)

@app.route('/score')
def score():
    name = session.get('name')
    id = session.get('id')
    grade = getgrades(id, name)
    parser(id, grade)
    return render_template( "/score/" + str(id) + ".html" )

# 注销
@app.route('/logout/')
def logout():
    session.clear()
    return redirect(url_for('login'))

@app.route('/studentlogin', methods=['GET', 'POST'])
def studentlogin():
    if request.method == 'GET':
        user = 1
        return render_template('login.html', user=user)
    else:
        id = request.form.get('id')
        password = str(request.form.get('password'))
        user = User.query.filter(User.id == id).first()
        if user:
            if check_password_hash(user.password, password):
                session['id'] = user.id
                session['name'] = user.name
                session['password'] = user.password
                session['user'] = 'student'
                return redirect(url_for('student'))
            else:
                return redirect(url_for('login'))
        else:
            username = spider_login(id, password)
            score_path = "/score/"  + str(id) + ".html"
            password = generate_password_hash(password)
            user = User(id, password, username, score_path)
            db.session.add(user)
            db.session.commit()
            session['id'] = id
            session['name'] = username
            session['password'] = password
            session['user'] = 'student'
            return redirect(url_for('student'))


@app.route('/student', methods=['GET', 'POST'])
def student():
    if request.method == 'GET':
        return render_template('student.html')
    else:
        return render_template('student.html')












@app.route('/teacherlogin', methods=['GET', 'POST'])
def teacherlogin():
    if request.method == 'GET':
        user = 0
        return render_template('login.html', user=user)
    else:
        id = request.form.get('id')
        password = str(request.form.get('password'))
        tea = Teacher.query.filter(Teacher.id == id).first()
        if tea:
            if password == tea.password:
                session['id'] = id
                session['user'] = 'teacher'
                return redirect(url_for('teacher'))
        else:
            return render_template('login.html', user=user)
            
@app.route('/teacher', methods=['GET', 'POST'])
def teacher():
    if request.method == 'GET':
        return render_template('teacher.html')
    else:
        return render_template('teacher.html')

if __name__ == "__main__":
    app.run()
