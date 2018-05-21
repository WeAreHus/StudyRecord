# -*- coding: utf-8 -*-
from flask import Blueprint, render_template, redirect

students = Blueprint('students',__name__)

#显示学生个人成绩信息页面，可输入学生姓名进行成个人信息查询
@students.route('/PersonalInformation', methods=['GET'])
def PersonalInformation():
    return render_template('Pinformation.html')

@students.route('/grxxcx', methods=['POST'])
def grxxcx():
    pass

#显示学生成绩查询页面，输入学生姓名即可进行成绩查询
@students.route('/selectgrades', methods=['GET'])
def selectgrades():
    return render_template('selectgrades.html')

@students.route('cjcx', methods=['POST'])
def cjcx():
    pass
