DEBUG = True

HOST = "127.0.0.1"
PORT = "3306"
DB = "moredemo"
USER = "fty"
PASS = "674099"
CHARSET = "utf8"
DB_URI = "mysql+mysqldb://{}:{}@{}:{}/{}?charset={}".format(USER, PASS, HOST, PORT, DB, CHARSET)
SQLALCHEMY_DATABASE_URI = DB_URI

SECRET_KEY = "THIS-A-SECRET-KEY"

MAX_CONTENT_LENGTH = 1 * 1024 * 1024