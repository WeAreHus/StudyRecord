# encoding: utf-8
import os
import shutil
import sys
import time

import requests
from pyecharts import Line

reload(sys)
sys.setdefaultencoding('utf-8')


def chart(lists):
    bar = Line("学生成绩平均绩点折线图")
    bar.add("平均绩点GPA", ["大一（上）", "大一（下）", "大二（上）", "大二（下）", "大三（上）", "大三（下）"], [
            lists[0], lists[1], lists[2], lists[3], lists[4], lists[5]], is_more_utils=True)
    bar.show_config()
    bar.render()
    shutil.move('/home/fty/new-system/render.html',
                '/home/fty/new-system/templates/student.html')

    file = ""
    with open('/home/fty/new-system/templates/student.html', 'r') as f:
        hello = f.read()
        file = hello
        f.close()

    head = '''
    {% extends 'base.html' %}
    {% block page_name %}你好,{{login_user}}{% endblock %}
    {% block body_part3 %}
    <a href="{{ url_for('student') }}" class="nav-link active">
    {% endblock %}
    {% block body_part1 %}你好,{{login_user}}{% endblock %}
    {% block body_part2 %}
    '''
    with open('/home/fty/new-system/templates/student.html', 'w') as f1:
        f1.write(head)
        f1.write(file)
        f1.write('\n')
        f1.write("{% endblock %}")
