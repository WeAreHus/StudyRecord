#coding:utf8
# 数据库迁移的文件
# flask-script让我们可以使用命令行去完成数据库迁移的操作
from flask_script import Manager
from flask_migrate import Migrate, MigrateCommand
from view import app, db
from models import Student, Teacher

manager = Manager(app)

migrate = Migrate(app, db)

manager.add_command('db', MigrateCommand)


if __name__ == '__main__':
    manager.run()