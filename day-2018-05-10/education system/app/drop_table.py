#!/usr/bin/python
# encoding: utf-8
import MySQLdb
# 打开数据库连接
conn = MySQLdb.connect(host="localhost", user="man_user", passwd="674099", db="snailblog")
# 使用cursor()方法获取操作游标
cursor = conn.cursor()

# 如果数据表已经存在使用 execute() 方法删除表。
cursor.execute("DROP TABLE IF EXISTS user")

cursor.execute("DROP TABLE IF EXISTS classes")


cursor.execute("DROP TABLE IF EXISTS scores")

cursor.execute("DROP TABLE IF EXISTS user_to_classes")

conn.close()