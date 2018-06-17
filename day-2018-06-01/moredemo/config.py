# coding:utf8

# 开启调试模式
DEBUG = True
#开启多线程
threaded=True

# 数据库信息
HOST = "127.0.0.1"
PORT = "3306"
DB = "moredemo"
USER = "fty"
PASS = "674099"
CHARSET = "utf8"
# python2默认使用mysqldb,如果为python3则需要更改为pymysql
DB_URI = "mysql+mysqldb://{}:{}@{}:{}/{}?charset={}".format(USER, PASS, HOST, PORT, DB, CHARSET)
SQLALCHEMY_DATABASE_URI = DB_URI

# 使用flash需要的配置操作
SECRET_KEY = "THIS-A-SECRET-KEY"

# 限制上传的文件大小（2G）
MAX_CONTENT_LENGTH = 2 * 1024 * 1024 * 1024