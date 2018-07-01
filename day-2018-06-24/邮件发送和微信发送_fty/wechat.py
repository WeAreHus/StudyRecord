# -*- coding: UTF-8 -*-
# 给指定联系人发送消息
import itchat

itchat.auto_login(hotReload=True)  # 首次扫描登录后后续自动登录

# name为备注名
users = itchat.search_friends(name=u'李细鹏学长')
userName = users[0]['UserName']
itchat.send("This is a test",toUserName = userName)