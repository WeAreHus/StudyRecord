#coding:utf8
from flask import Flask, render_template, request, flash, session, url_for, redirect, g, Response
from models import db, Users, Questions, Comments
from werkzeug.security import generate_password_hash
from sqlalchemy import or_
from os import path
import os
from werkzeug import secure_filename

from exts import validate, validate_func, allowed_file
import config

app = Flask(__name__)
# 提交配置文件
app.config.from_object(config)
db.init_app(app)

with app.test_request_context():
    db.create_all()

# 上下文管理器
@app.context_processor
def my_context_processor():
    # 判断是否有用户登录，即g中user是否有内容
    if hasattr(g, 'user'):
        return {'login_user': g.user}
    return {}

# 钩子函数，每一次请求都会执行一次，得到当前登录用户的User对象
@app.before_request
def my_before_request():
    # 使用flask的session获取登录用户的用户名
    username = session.get('username')
    # 判断条件，如果有用户已经登录，则通过query语句返回对应的用户对象，并保存在g对象中(g对象不能跨请求使用)
    if username:
        g.user = Users.query.filter(Users.username == username).first()

@app.route('/')
def home():
    # query语句，按照questions表中create_time字段降序排序返回
    questions = Questions.query.order_by(Questions.create_time.desc()).all()
    return render_template('home.html', questions=questions)

# 注册
@app.route('/register/', methods=['GET', 'POST'])
def register():
    if request.method == 'GET':
        return render_template('register.html')
    else:
        # 以POST方法提交表单
        username = request.form.get('username')
        password1 = request.form.get('password1')
        password2 = request.form.get('password2')
        # 返回操作结果指示
        message = validate(username, password1, password2)
        # 将message的内容显示在html上
        flash(message)
        # 如果message中有successful的字符串
        if 'f' in message:
            # 新建Users表对象，密码加密
            new_user = Users(username=username, password=generate_password_hash(password1))
            db.session.add(new_user)
            db.session.commit()
            session['status'] = 'OK'
            return redirect(url_for('login'))
        else:
            session['status'] = 'BAD'
            return render_template('register.html')

# 登录
@app.route('/login/', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        return render_template('login.html')
    else:
        username = request.form.get('username')
        password = request.form.get('password1')
        # 返回操作结果指示
        message = validate(username, password)
        if 'f' in message:
            session['username'] = username
            session.permanent = True
            session['status'] = 'OK'
            return redirect(url_for('home'))
        else:
            flash(message)
            session['status'] = 'BAD'
            return render_template('login.html')

# 注销
@app.route('/logout/')
def logout():
    session.clear()
    return redirect(url_for('home'))

# 发布问答
@app.route('/question/', methods=['GET', 'POST'])
def question():
    if request.method == 'GET':
        return render_template('question.html')
    else:
        # 判断当前是否已有用户登录
        if hasattr(g, 'user'):
            question_title = request.form.get('question_title').strip()
            question_desc = request.form.get('question_desc').strip()
            # 获取g对象中保存的user对象的id属性
            author_id = g.user.id
            new_question = Questions(title=question_title, content=question_desc, author_id=author_id)
            db.session.add(new_question)
            db.session.commit()
            return redirect(url_for('home'))
        else:
            flash('Please log in first')
            return redirect(url_for('login'))

# url传参，评论功能
@app.route('/details/<question_id>/', methods=['GET', 'POST'])
def details(question_id):
    if request.method == 'GET':
        # 获取点击对象的question_id
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

# 导航栏中的搜索功能
@app.route('/search')
def search():
    # 获取GET数据，注意和获取POST数据的区别
    # 搜索框输入的关键字
    keyword = request.args.get('keyword')
    # 使用Model.Column.Contains(keyword)与filter结合来筛选指定的Column字段包含keyword的内容
    # 从sqlalchemy到处or_函数，表示或的关系
    result = Questions.query.filter(or_(Questions.title.contains(keyword),
                                    Questions.content.contains(keyword))).order_by(
                                    Questions.create_time.desc()).all()
    if result:
        return render_template('home.html', questions=result, search_title=True)
    else:
        return render_template('warn.html')

# 用户中心
@app.route('/user/', methods=['GET', 'POST'])
def user_center():
    return render_template('user.html')

# 修改密码
@app.route('/user/security/', methods=['GET', 'POST'])
def security():
    if request.method == 'GET':
        return render_template('security.html')
    else:
        o_password = request.form.get('o_password')
        password1 = request.form.get('password1')
        password2 = request.form.get('password2')
        message = validate_func(g.user, o_password, password1, password2)   
        if 'f' in message:
            g.user.password = generate_password_hash(password1)
            db.session.commit()
            session.clear()
            flash(message)
            session['status'] = 'OK'
            return redirect(url_for('logout'))
        else:
            flash(message)
            session['status'] = 'BAD'
            return render_template('security.html')

# 上传头像,上传文件用到POST方法
@app.route('/user/avatar/', methods=['GET', 'POST'])
def avatar():
    if request.method == 'POST':
        # 获取上传的文件,avatar_upload为对应input标签的name属性
        file = request.files['avatar_upload']
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            # 用os库的path,处理路径相关的东西
            base_path = path.abspath(path.dirname(__file__))
            # 将图片以用户id的形式命名，防止同名覆盖
            filename = str(g.user.id) + '.' + filename.rsplit('.', 1)[1]
            file_path = path.join(base_path, 'static', 'images', 'uploads', filename)
            # 使用文件的save(具体路径)方法保存,默认不会保存到py文件所在的路径，而是系统的根目录
            file.save(file_path)
            g.user.avatar_path = 'images/uploads/' + filename
            db.session.commit()
    return render_template('avatar.html', user=g.user)

# 接收上传的分片，并保存在本地
@app.route('/file/upload', methods=['GET','POST'])
def upload_part():                              # 接收前端上传的一个分片
    if request.method == 'POST':
        task = request.form.get('task_id')          # 获取文件的唯一标识符
        chunk = request.form.get('chunk', 0)        # 获取该分片在所有分片中的序号
        filename = '%s%s' % (task, chunk)           # 构造该分片的唯一标识符

        upload_file = request.files['file']
        upload_file.save('./upload/%s' % filename)  # 保存分片到本地
    return render_template('upload.html')

# 将所有分片内容写入新文件
@app.route('/file/merge', methods=['GET'])
def upload_success():                                   # 按序读出分片内容，并写入新文件
    target_filename = request.args.get('filename')      # 获取上传文件的文件名
    task = request.args.get('task_id')                  # 获取文件的唯一标识符
    chunk = 0  # 分片序号
    with open('./upload/%s' % target_filename, 'wb') as target_file:  # 创建新文件
        while True:
            try:
                filename = './upload/%s%d' % (task, chunk)
                source_file = open(filename, 'rb')      # 按序打开每个分片
                target_file.write(source_file.read())   # 读取分片内容写入新文件
                source_file.close()
            except IOError:
                break

            chunk += 1
            os.remove(filename)                         # 删除该分片，节约空间

    return render_template('upload.html')

# 获取器upload目录文件列表
@app.route('/file/list', methods=['GET'])
def file_list():
    files = os.listdir('./upload/')  # 获取文件目录
    files = map(lambda x: x if isinstance(x, unicode) else x.decode('utf-8'), files)  # 注意编码
    return render_template('list.html', files=files)

# 实现点击文件名下载对应文件
@app.route('/file/download/<filename>', methods=['GET'])
def file_download(filename):
    def send_chunk():  # 流式读取
        store_path = './upload/%s' % filename
        with open(store_path, 'rb') as target_file:
            while True:
                chunk = target_file.read(20 * 1024 * 1024)
                if not chunk:
                    break
                yield chunk

    return Response(send_chunk(), content_type='application/octet-stream')

if __name__ == '__main__':
    app.run()