#!/usr/bin/python
# -*- coding: UTF-8 -*-
# 使用QQ的SMTP服务器代理发送邮件

import smtplib
from email.mime.text import MIMEText
from email.utils import formataddr

def sendemail(my_user, user_name, n):
    my_sender='2505888537@qq.com'    # 发件人邮箱账号
    my_pass = 'XXXXXXXXXX'              # 发件人邮箱授权码
    ret=True
    try:
        msg=MIMEText(n,'html','utf-8')
        msg['From']=formataddr(["教务系统",my_sender])  # 括号里的对应发件人邮箱昵称、发件人邮箱账号
        msg['To']=formataddr([user_name,my_user])              # 括号里的对应收件人邮箱昵称、收件人邮箱账号
        msg['Subject']="你的成绩单"                # 邮件的主题，也可以说是标题

        server=smtplib.SMTP_SSL("smtp.qq.com", 465)  # 发件人邮箱中的SMTP服务器，端口是25
        server.login(my_sender, my_pass)  # 括号中对应的是发件人邮箱账号、邮箱密码
        server.sendmail(my_sender,[my_user,],msg.as_string())  # 括号中对应的是发件人邮箱账号、收件人邮箱账号、发送邮件
        server.quit()  # 关闭连接
    except Exception:  # 如果 try 中的语句没有执行，则会执行下面的 ret=False
        ret=False
        
    if ret:
        return True
    else:
        return False
