## SQLALchemy操作
---
[TOC]
### ORM框架
---
&emsp;&emsp;如果写程序用pymysql和程序交互，那是不是要写原生sql语句。如果进行复杂的查询，那sql语句就要进行一点一点拼接，而且不太有重用性，扩展不方便。而且写的sql语句可能不高效，导致程序运行也变慢。
 
&emsp;&emsp;为了避免把sql语句写死在代码里，有没有一种方法直接把原生sql封装好了并且以你熟悉的方式操作，像面向对象那样？ 

&emsp;&emsp;数据库表是一个二维表，包含多行多列。把一个表的内容用Python的数据结构表示出来的话，可以用一个list表示多行，list的每一个元素是tuple，表示一行记录，比如下表:

| id    | name   | password |
| :-------- | --------:| :--: |
| 111 | Tom        | 111      |
| 112 | Alen       | 112      |
| 123 | Jarry      | 123      |
| 222 | Ben        | 222      |
| 666 | ABC        | 666      |
| 777 | Clearlove7 | 777      |

可以表示为:
```
[
(111, ‘Tom’, ‘111’),
(112, ‘Alen’, ‘112’),
(123, ‘Jarry’, ‘123’),
(222, ‘Ben’, ‘222’),
(666, ‘ABC’, ‘666’),
(777, ‘Clearlove7’, ‘777’)
]
```
&emsp;&emsp;但是用tuple表示一行很难看出表的结构。如果把一个tuple用class实例来表示，就可以更容易地看出表的结构来：
```python
class Student(object):
	def __init__(self, id, name, password):
		self.id = id
		self.name = name
		self.password = password

[
	Student(111, ‘Tom’, ‘111’),
	Student (112, ‘Alen’, ‘112’),
	Student (123, ‘Jarry’, ‘123’),
	Student (222, ‘Ben’, ‘222’),
	Student (666, ‘ABC’, ‘666’),
	Student (777, ‘Clearlove7’, ‘777’)
]
```
&emsp;&emsp;这就是传说中的ORM技术：Object-Relational Mapping，把关系数据库的表结构映射到对象上,ORM 相当于把数据库也给你实例化了，在代码操作mysql中级又加了orm这一层。 在Python中，最有名的ORM框架是SQLAlchemy。我们来看看SQLAlchemy的用法。

### 如何安装SQLAlchemy?
---
使用pip安装：`pip install sqlalchemy`

使用easy_install安装：`easy_install sqlalchemy`

或者执行：

`http://pypi.douban.com/packages/source/S/SQLAlchemy/SQLAlchemy-0.9.3.tar.gz`

`tar -xzvf SQLAlchemy-0.9.3.tar.gz`

`cd SQLAlchemy-0.9.3 `

`sudo python setup.py install`

### 建表
---
第一步，导入SQLAlchemy
```python
# -*- coding: UTF-8 -*-
# 导入:
from sqlalchemy import Column, String, Integer, create_engine, ForeignKey
from sqlalchemy.orm import sessionmaker, relationship
from sqlalchemy.ext.declarative import declarative_base
```
在使用中我们需要用到什么就导入什么
```python
# 初始化数据库连接:
engine = create_engine('mysql+mysqldb://man_user:674099@localhost:3306/snailblog')
# 创建对象的基类:
Base = declarative_base()
# 创建DBSession类型
# 创建与数据库的会话DBSession,注意,这里返回的是个class,不是实例,实例和engine绑定
DBSession = sessionmaker(bind=engine)
```
生成的DBSession是个类，与engine绑定。

其他的连接驱动：
```
MySQL-Python
    mysql+mysqldb://<user>:<password>@<host>[:<port>]/<dbname>

pymysql
    mysql+pymysql://<username>:<password>@<host>/<dbname>[?<options>]

MySQL-Connector
    mysql+mysqlconnector://<user>:<password>@<host>[:<port>]/<dbname>

cx_Oracle
    oracle+cx_oracle://user:pass@host:port/dbname[?key=value&key=value...]
```
至此，我们可以开始定义需要建立的表了。
```python
# 定义User对象:
class User(Base):
    # 表的名字:
    __tablename__ = 'user'

    # 表的结构:
    id = Column(Integer, nullable=False, primary_key=True)
    name = Column(String(20), nullable=False)
```
如果有其他的表则继续建立class。

表定义完毕后使用类方法：
```python
#创建表结构 （这里是父类调子类）
Base.metadata.create_all(engine)
```
数据库中已经存在该表的话就不会重复建立了。

所有操作完毕后，运行脚本则建表完成，当然如果需要删除已建立的表可以使用：
```python
Base.metadata.drop_all(engine)
```

### 插入
---
我们数据表建好后如何向其中插入数据呢？
```python 
# 创建session对象：
session = DBsession()
# 创建新User对象：
new_user1 = User(id = '1', name = 'Bob')
# 添加到session，批量操作使用add_all():
session.add(new_user1)
new_user2 = User(id = '2', name = 'Jarry')
new_user3 = User(id = '3', name = 'Lucy')
session.add_all([new_user2, new_user3])
# 提交即保存到数据库：
session.commit()
```
生成session实例，相当于游标，用于插入或查询操作，注意,这里返回给session的是个class,不是实例。

也可以直接由sessionmaker建立（需要engine）：
```python
session = sessionmaker(bind = engine)
```
上方代码向user表插入了3行数据。

在没有其他操作后，我们可以使用：
```python
# 关闭Session:
session.close()
```

### 查询、修改和删除
---
```python
# 创建Query查询，filter是where条件，最后调用one()返回唯一行，如果调用all()则返回所有行:
user = session.query(User).filter(User.id=='5').one()	#filter_by方法判断相等使用'='
# 打印类型和对象的name属性:
print 'type:', type(user)	#返回的user是个对象
print 'name:', user.name	#调用user的属性

user = session.query(User).all()
# 打印类型和对象的name属性:
print "-------all-------"
print 'type:', type(user)	#返回的user是个列表
print 'user:', user[0]
print 'name:', user[0].name
```
&emsp;&emsp;不要关闭session，我们继续查询操作。

&emsp;&emsp;我们可以使用session.query（table_name）方法查询数据表里的信息，filter的作用相当于sql语句中的where，filter()判断相等使用‘=’，而filter_by()判断相等使用’==’。

如果有多个控制条件则可以多次使用filter，例如：
```
user = session.query(User).filter(User.id = ‘1’).filter(User.name = ‘Bob’).one()
```
  （**提示：单纯的查询操作不需要session.commit()）**
  
**query查询中使用过滤器(filter的一些方法) (即session.query.filter(……))**
```
### Common Filter Operators------------------------------------
#equals:
 query.filter(User.name == 'ed')
#------------------------------------
# not equals:
 query.filter(User.name != 'ed')
#------------------------------------
# LIKE:
 query.filter(User.name.like('%ed%'))
#------------------------------------
# IN:
 query.filter(User.name.in_(['ed', 'wendy', 'jack']))
#------------------------------------
# NOT IN:
 query.filter(~User.name.in_(['ed', 'wendy', 'jack']))
#------------------------------------
# IS NULL:
 query.filter(User.name == None)
```
使用**textual sql**进行选择，允许用于自定义查询语句
```
session.query(User).from_statement(text("select * from user")).all()
```
&emsp;&emsp;我们如何修改其中的数据呢？

&emsp;&emsp;这很简单，我们使用session.query()返回对象后直接对需要更改的属性进行赋值即可。
```
user[0].name = 'Tom'
session.commit()
```
**（不要忘记commit()提交到数据库）**

同样的，删除数据也十分简单：
```
#获取对象之后删除
x = session.query(User).filter(User.id == '3').one()
session.delete(x)
session.commit()
```
**(注意：所有操作最终不要忘记关闭session)**

### 控制打印输出
---
&emsp;&emsp;我们在使用query()方法返回实例对象后想打印查看里面的内容每次调用其中的属性看起来会有些麻烦，所以我们可以使用**__repr__**方法控制print语句输出的内容。
```python
# 定义User对象:
class User(Base):
    # 表的名字:
    __tablename__ = 'user'

    # 表的结构:
    id = Column(Integer, nullable=False, primary_key=True)
    name = Column(String(20), nullable=False)
    #控制打印
    def __repr__(self):
        return "<User(id = '%s', name = '%s', password = '%s')>" % (self.id, self.name, self.password)
```
这样，我们在print user 时就可以按照我们定义的样式打印了：
```
<User(id = '1', name = 'Bod')>
```

### 外键关联
---
&emsp;&emsp;我们关联两个表一般使用外键，那么我们如何使用sqlalchemy设置外键呢？其实也很简单，我们一起来看。

&emsp;&emsp;首先导入两个相关包：
```
from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship
```
设想：我们希望可以查看不同学生的上课记录要如何实现？

&emsp;&emsp;一名学生可以有多个上课记录，一个上课记录只对一名学生，所以这是个一对多的关系。不管如何，我们肯定要建立两个表，一个保存学生信息一个保存上课记录：
```python
engine = create_engine('mysql+mysqldb://man_user:674099@localhost:3306/snailblog')
Base = declarative_base()  # 生成orm基类

class Stu(Base):
    __tablename__ = "stu"
    id = Column(BIGINT, primary_key=True)
    name = Column(String(32),nullable=False)
    register_date = Column(DATE,nullable=False)
    def __repr__(self):
        return "<id:%s name:%s>" % (self.id, self.name)

class StudyRecord(Base):
    __tablename__ = "study_record"
    id = Column(Integer, primary_key=True)
    day = Column(Integer,nullable=False)
    status = Column(String(32),nullable=False)
    stu_id = Column(BIGINT,ForeignKey("stu.id"))  #------外键关联------
    #这个允许你在user表里通过backref字段反向查出所有它在stu2表里的关联项数据
    stu = relationship("Stu", backref="my_study_record")  # 添加关系，反查（在内存里）
    def __repr__(self):
        return "<name:%s day:%s status:%s>" % (self.stu.name, self.day,self.status)

Base.metadata.create_all(engine)  # 创建表结构

Session_class = sessionmaker(bind=engine)
```
&emsp;&emsp;在上图的study_record表中的stu_id属性中的ForeignKey("stu.id")就是外键的定义，这里定义了study_record表通过stu.id作为外键与stu表关联。

&emsp;&emsp;在其下方：
```
stu = relationship("Stu", backref="my_study_record")
```
&emsp;&emsp;添加了关系，并设置反查属性名为"my_study_record"，之后我们可以借助它从stu表查到study_record的信息。

&emsp;&emsp;我们可以看看表的属性：

![stu表](https://github.com/CANYOUFINDIT/myproject/blob/master/markdown/stu.png)

![study_record表](https://github.com/CANYOUFINDIT/myproject/blob/master/markdown/rec.png)


现在我们想两个表中插入一些数据：
```python
session = Session_class()  # 生成session实例 #cursor

s1 = Stu(name="A",register_date="2014-05-21")
s2 = Stu(name="J",register_date="2014-03-21")
s3 = Stu(name="R",register_date="2014-02-21")
s4 = Stu(name="E",register_date="2013-01-21")

study_obj1 = StudyRecord(day=1,status="YES", stu_id=1)
study_obj2 = StudyRecord(day=2,status="NO", stu_id=1)
study_obj3 = StudyRecord(day=3,status="YES", stu_id=1)
study_obj4 = StudyRecord(day=1,status="YES", stu_id=2)

session.add_all([s1,s2,s3,s4,study_obj1,study_obj2,study_obj3,study_obj4])  # 创建

session.commit()
```
看看插入结果：
![插入结果](https://github.com/CANYOUFINDIT/myproject/blob/master/markdown/1.png)

我们现在查询看看：
```python
stu_obj = session.query(Stu).filter(Stu.name=="A").first()  # 查询
print stu_obj
# 在stu2表，查到StudyRecord表的记录
print(stu_obj.my_study_record)  # 查询A一共上了几节课
```
```
<id:1 name:A>
[<name:A day:1 status:YES>, <name:A day:2 status:NO>, <name:A day:3 status:YES>]
```
可以看到query()返回对象的my_study_record属性包含了study_record表的内容。

### 多对多外键关联
---
&emsp;&emsp;上文中我们了解了一对多的外键关联，现在我们再来看看多对多关系的外键关联。

&emsp;&emsp;我们从一个例子来入手：一名作者(authors)可以有多本作品(books)，一本书也可以有多个作者参与完成，那么我们如何将二者关联？

&emsp;&emsp;其实我们在建立一个中间表(book_m2m_author)将二者连接上就行了，我们一起来操作一下。

引包：
```
#foreignkey.py
from sqlalchemy import Table, Column, Integer,String,DATE, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
```
作者表(authors)：
```python
Base = declarative_base()
class Author(Base):
    __tablename__ = 'authors'
    id = Column(Integer, primary_key=True)
    name = Column(String(32))
    def __repr__(self):
        return self.name
```
作品表(books)：
```python
class Book(Base):
    __tablename__ = 'books'
    id = Column(Integer,primary_key=True)
    name = Column(String(64))
    pub_date = Column(DATE)
    # book表不知道第三张表，所以关联一下第三张表
    authors = relationship('Author',secondary=book_m2m_author,backref='books')
    def __repr__(self):
        return self.name
```
中间表(book_m2m_author)：
```
# 第三张表 自己创建。不需要手动管理，orm自动维护
book_m2m_author = Table('book_m2m_author', Base.metadata,
                        Column('book_id',Integer,ForeignKey('books.id')),
                        Column('author_id',Integer,ForeignKey('authors.id')),
                        )
```
&emsp;&emsp;中间表保存了两个表的主键作为外键，在book表中建立与author的relationship并添加secondary属性值为中间表名，添加反查属性名为books。

&emsp;&emsp;建表的部分完成，我们向里面插几条数据看看。

&emsp;&emsp;因为建表部分我写在foreignkey.py中，所以在操作时需要调用其内容。
```python
#foreignkey_insert.py
import foreignkey
from sqlalchemy.orm import sessionmaker

Session_class = sessionmaker(bind=foreignkey.engine)  # 创建与数据库的会话session class ,注意,这里返回给session的是个class,不是实例
session = Session_class()  # 生成session实例 #cursor
# 创建书

b1 = foreignkey.Book(name="The First Demo",pub_date="2018-04-24")
b2= foreignkey.Book(name="The Second Demo",pub_date="2018-04-25")
b3 = foreignkey.Book(name="The Third Demo",pub_date="2018-04-26")
# 创建作者
a1 = foreignkey.Author(name="Futongyong")
a2 = foreignkey.Author(name="Chenwei") 
a3 = foreignkey.Author(name="Xiangjinhu")
# 关联关系
b1.authors = [a1,a3]
b2.authors = [a2,a3]
b3.authors = [a1,a2,a3]

session.add_all([b1,b2,b3,a1,a2,a3])

session.commit()
session.close()
```
以上信息可以明了：
| book            | author1       | author2      | author3   |
| :-              | :-:           |  :-:         | :-:       |
| The First Demo  | Futongyong    | Xiangjinhu   | NULL      |
| The Second Demo | Chenwei       | Xiangjinhu   | NULL      |
| The Third Demo  | Futongyong    | Chenwei      | Xiangjinhu|
现在来查询看看：
```python
#foreignkey_query.py
# -*- coding: UTF-8 -*-
# 查询数据
import foreignkey
from sqlalchemy.orm import sessionmaker

Session_class = sessionmaker(bind=foreignkey.engine)  # 创建与数据库的会话session class ,注意,这里返回给session的是个class,不是实例
session = Session_class()  # 生成session实例 #cursor

#查询
author_obj = session.query(foreignkey.Author).filter(foreignkey.Author.name=="Futongyong").first()
print(author_obj.books)
book_obj = session.query(foreignkey.Book).filter(foreignkey.Book.id==1).first()
print(book_obj.authors)

session.close()
```
&emsp;&emsp;第一句查询作者为Futongyong的book；

&emsp;&emsp;第二句查询id为1的book的作者；

结果：
```
[The First Demo, The Third Demo]
[Futongyong, Xiangjinhu]
```
&emsp;&emsp;跟我们预期的一样哦。

&emsp;&emsp;现在我们又有个问题：如果我们在录入信息的时候操作错误比如多录入了一个作者，该如何将他删除呢？
```python
#foreignkey.delect.py
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
```
&emsp;&emsp;在第一个删除操作中，我们删除了The First Demo中的一个作者Futongyong；

&emsp;&emsp;在第二个删除操作中，我们直接删除了Futognyong，所以最终所有的book中都不会有他的身影了。

