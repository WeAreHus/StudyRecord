"""
from flask import Flask    # 不用多说
from main import admin,students    #导入blueprints目录下musics.py与movies.py模块,
 
app=Flask(__name__)    #创建 Flask()对象： app
 
@app.route('/')  #使用了蓝图，app.route() 这种模式就仍可以使用，注意路由重复的问题
def hello_world():
    return 'hello my world !'
 
app.register_blueprint(admin.admin)     # 将musics模块里的蓝图对象musics注册到app
app.register_blueprint(students.students)     # 将movies模块里的蓝图对象movies注册到app
"""



from flask import Blueprint
 
main = Blueprint('main', __name__) 
 
from . import views, errors, admin, students

def create_app(config_name): 
  # ...
  from .main import main as main_blueprint 
  app.register_blueprint(main_blueprint)
 
  return app

def create_app(config_name):
 # ...
  from .auth import auth as auth_blueprint
  app.register_blueprint(auth_blueprint, url_prefix='/admin')
  return app

def create_app(config_name):
 # ...
  from .auth import auth as auth_blueprint
  app.register_blueprint(auth_blueprint, url_prefix='/students')
  return app