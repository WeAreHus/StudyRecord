import pymysql 
from flask import Flask
from flask import render_template
from flask import request   
import traceback

db = pymysql()

def create_app(config_name):
    app = Flask(__name__)
    app.config.from.object(config[config_name])
    config[config_name].init_app(app)
    db.init_app(app)
    return app
