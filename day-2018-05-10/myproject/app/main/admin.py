# -*- coding: utf-8 -*-
from flask import Blueprint,render_template, request

admin = Blueprint('admin',__name__)

#插入学生成绩
@admin.route('/InsertGrades', methods=['GET'])
def Insertgrades():
    return render_template('Insertgrades.html')

@admin.route('crxscj',methods=['POST'])
def crxscj():
        pass


#学生成绩修改
@admin.route('/ChangeGrades', methods=['GET'] )
def ChangeGrades():
    return render_template('ChangeGrades.html')

@admin.route('xgxscj'， methods=['POST'])
def xgxscj():
    pass


#学生成绩删除
@admin.route('/DeleteGrades', methods=['GET'])
def DeleteGrades():
    return render_template('DeleteGrades.html')

@admin.route('scxscj', methods=['POST'])
def scxscj():
    pass
