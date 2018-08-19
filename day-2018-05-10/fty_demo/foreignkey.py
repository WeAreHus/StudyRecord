# -*- coding: UTF-8 -*-
# 创建表结构
from sqlalchemy import Table, Column, Integer,String,DATE, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

Base = declarative_base()
# 第三张表 自己创建。不需要手动管理，orm自动维护
book_m2m_author = Table('book_m2m_author', Base.metadata,
                        Column('book_id',Integer,ForeignKey('books.id')),
                        Column('author_id',Integer,ForeignKey('authors.id')),
                        )
class Book(Base):
    __tablename__ = 'books'
    id = Column(Integer,primary_key=True)
    name = Column(String(64))
    pub_date = Column(DATE)
    # book表不知道第三张表，所以关联一下第三张表
    authors = relationship('Author',secondary=book_m2m_author,backref='books')
    def __repr__(self):
        return self.name

class Author(Base):
    __tablename__ = 'authors'
    id = Column(Integer, primary_key=True)
    name = Column(String(32))
    def __repr__(self):
        return self.name

engine = create_engine('mysql+mysqldb://man_user:674099@localhost:3306/snailblog')

Base.metadata.create_all(engine)  # 创建表结构
#Base.metadata.drop_all(engine)