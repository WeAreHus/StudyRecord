# -*- coding: UTF-8 -*-
# 删除数据
import foreignkey
from sqlalchemy.orm import sessionmaker

Session_class = sessionmaker(bind=foreignkey.engine)  # 创建与数据库的会话session class ,注意,这里返回给session的是个class,不是实例
session = Session_class()  # 生成session实例 #cursor

#通过书删除作者
author_obj =session.query(foreignkey.Author).filter_by(name="Futongyong").first()
book_obj = session.query(foreignkey.Book).filter_by(name="The First Demo").first()
book_obj.authors.remove(author_obj) #从一本书里删除一个作者
session.commit()

#直接删除作者,删除作者时，会把这个作者跟所有书的关联关系数据也自动删除
author_obj =session.query(foreignkey.Author).filter_by(name="Futongyong").first()
# print(author_obj.name , author_obj.books)
session.delete(author_obj)
session.commit()