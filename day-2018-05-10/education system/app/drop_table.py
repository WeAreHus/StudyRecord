#!/usr/bin/python
# encoding: utf-8
import MySQLdb
# 打开数据库连接
conn = MySQLdb.connect(host="localhost", user="man_user", passwd="674099", db="snailblog")
# 使用cursor()方法获取操作游标
cursor = conn.cursor()

# 如果数据表已经存在使用 execute() 方法删除表。
sql = """DROP TABLE IF EXISTS user;
        CREATE TABLE `user` (
          `id` int(11) NOT NULL AUTO_INCREMENT,
          `name` varchar(10) NOT NULL,
          `birthday` int(11) DEFAULT NULL,
          `collage` varchar(20) DEFAULT NULL,
          `major` varchar(20) DEFAULT NULL,
          `grade` int(11) DEFAULT NULL,
          `password` varchar(20) NOT NULL,
          `power` int(11) DEFAULT NULL,
          PRIMARY KEY (`id`)
        ) ENGINE=InnoDB DEFAULT CHARSET=latin1
"""
cursor.execute(sql)

sql = """DROP TABLE IF EXISTS classes;
        CREATE TABLE `classes` (
          `id` int(11) NOT NULL AUTO_INCREMENT,
          `name` varchar(20) NOT NULL,
          PRIMARY KEY (`id`)
        ) ENGINE=InnoDB DEFAULT CHARSET=latin1
"""
cursor.execute(sql)

sql = """DROP TABLE IF EXISTS scores;
        CREATE TABLE `scores` (
          `id` int(11) NOT NULL AUTO_INCREMENT,
          `fraction` int(11) NOT NULL,
          `user_id` int(11) DEFAULT NULL,
          `class_id` int(11) DEFAULT NULL,
          PRIMARY KEY (`id`),
          KEY `user_id` (`user_id`),
          KEY `class_id` (`class_id`),
          CONSTRAINT `scores_ibfk_1` FOREIGN KEY (`user_id`) REFERENCES `user` (`id`),
          CONSTRAINT `scores_ibfk_2` FOREIGN KEY (`class_id`) REFERENCES `classes` (`id`)
        ) ENGINE=InnoDB DEFAULT CHARSET=latin1
"""
cursor.execute(sql)

sql = """DROP TABLE IF EXISTS user_to_classes;
        CREATE TABLE `user_to_classes` (
          `user_id` int(11) DEFAULT NULL,
          `classes_id` int(11) DEFAULT NULL,
          KEY `user_id` (`user_id`),
          KEY `classes_id` (`classes_id`),
          CONSTRAINT `user_to_classes_ibfk_1` FOREIGN KEY (`user_id`) REFERENCES `user` (`id`),
          CONSTRAINT `user_to_classes_ibfk_2` FOREIGN KEY (`classes_id`) REFERENCES `classes` (`id`)
        ) ENGINE=InnoDB DEFAULT CHARSET=latin1
"""
cursor.execute(sql)

conn.close()