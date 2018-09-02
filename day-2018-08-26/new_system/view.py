# coding:utf8
from flask import (Flask, g, redirect, render_template, request, session,
                   url_for, flash)

import config
from models import Student, Score, Subject, db
from spider import spider_login, getgrades, get_timetable, parser, parser_timetable
from exts import sub_query, exts
from sendemail import sendemail
from matplot import chart

app = Flask(__name__)
app.config.from_object(config)
db.init_app(app)

with app.test_request_context():
    db.create_all()


@app.context_processor
def my_context_processor():
    if hasattr(g, 'user'):
        return {'login_user': g.user}
    return {}


@app.before_request
def my_before_request():
    id = session.get('id')
    name = session.get('name')
    if id:
        g.user = name



@app.route('/')
def login():
    return render_template('login.html', user=1)

# 注销
@app.route('/logout/')
def logout():
    session.clear()
    return redirect(url_for('login'))


@app.route('/studentlogin', methods=['GET', 'POST'])
def studentlogin():
    if request.method == 'GET':
        return render_template('login.html', user=1)
    else:
        try:
            id = request.form.get('id')
            password = str(request.form.get('password'))
            username = spider_login(id, password)
            user = Student.query.filter(Student.id == id).first()
            if user:
                pass
            else:
                user = Student(id, username)
                db.session.add(user)
                db.session.commit()
            parser(id, getgrades(id, username))
            session['id'] = id
            session['name'] = username
            session['user'] = 'student'
            return redirect(url_for('student'))
        except:
            flash('','error')
            return render_template('login.html', user=1)


@app.route('/student', methods=['GET', 'POST'])
def student():
    if request.method == 'GET':
        lists = [0,0,0,0,0,0,0,0]
        id = session.get('id')
        credit, cla = sub_query(id, '2016-2017', '1')
        lists[0] = credit[2]
        credit, cla = sub_query(id, '2016-2017', '2')
        lists[1] = credit[2]
        credit, cla = sub_query(id, '2017-2018', '1')
        lists[2] = credit[2]
        credit, cla = sub_query(id, '2017-2018', '2')
        lists[3] = credit[2]
        chart(lists)
        return render_template('student.html')
    else:
        return render_template('student.html')


@app.route('/score', methods=['GET', 'POST'])
def score():
    if request.method == 'GET':
        id = session.get('id')
        stu = Student.query.filter(Student.id == id).first()
        credit = exts(stu.subject)
        credit.append('all')
        credit.append('all')
        return render_template("score.html", classes=stu.subject, credit=credit)
    else:
        id = session.get('id')
        year = request.form.get('year')
        term = request.form.get('term')
        if year == 'all' and term == 'all':
            stu = Student.query.filter(Student.id == id).first()
            credit = exts(stu.subject)
            cla = stu.subject
        else:
            credit, cla = sub_query(id, year, term)
        credit.append(year)
        credit.append(term)
        return render_template("score.html", classes=cla, credit=credit)


@app.route('/timetable', methods=['GET', 'POST'])
def timetable():
    if request.method == 'GET':
        id = session.get('id')
        name = session.get('name')
        year = '2016-2017'
        term = '1'
        time_table = get_timetable(id, name, year, term)
        parser_timetable(time_table)
        return render_template('time_table.html', year=year, term=term)
    else:
        id = session.get('id')
        name = session.get('name')
        year = request.form.get('year')
        term = request.form.get('term')
        time_table = get_timetable(id, name, year, term)
        parser_timetable(time_table)
        return render_template('time_table.html', year=year, term=term)


@app.route('/email', methods=['GET', 'POST'])
def email():
    if request.method == 'GET':
        return render_template('sendemail.html')
    else:
        receive = request.form.get('email')
        id = session.get('id')
        name = session.get('name')
        grade = getgrades(id, name)
        if sendemail(receive, name, grade):
            flash('','OK')
            return render_template('sendemail.html')
        else:
            flash('','error')
            return render_template('sendemail.html')


@app.route('/wechat', methods=['GET', 'POST'])
def wechat():
    pass

if __name__ == "__main__":
    app.run()
