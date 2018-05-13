# -*- coding: UTF-8 -*-
'''
此demo意在展示一对多，多对一关系中的查询方法
数据库中表关系之间除了MySQL中标准的外键(ForeignKey)之外,还可以创建一个虚拟的关系,比如group = relationship("Group",backref='mygroup'),
一般此虚拟关系与foreignkey一起使用.

需求:

用户组,有sa,dba组
用户,用户只能属于一个用户组
那么从需求可以看出来,是一个一对多的
'''
from sqlalchemy import Table, Column, Integer,String,DATE, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

# 创建实例，并连接库
engine = create_engine('mysql+mysqldb://man_user:674099@localhost:3306/snailblog')

Base = declarative_base()

#一对多
class Group(Base):
    __tablename__ = 'group'
    gid = Column(Integer,primary_key=True,autoincrement=True)
    caption = Column(String(32))

class User(Base):
    __tablename__ = 'user'
    uid = Column(Integer,primary_key=True,autoincrement=True)
    name = Column(String(32))
    group_id = Column(Integer,ForeignKey('group.gid'))
    #创建虚拟关系,relationship  一般是跟foreginkey 在一起使用
    group = relationship("Group",backref='mygroup')

    #自定义输出方式
    def __repr__(self):
        temp = '%s-%s:%s'%(self.uid,self.name,self.group_id)
        return temp
 
Base.metadata.create_all(engine)
DBSession = sessionmaker(bind=engine)
session = DBSession()
'''
#添加
session.add_all([
    Group(caption='DBA'),
    Group(caption='SA')
 ])

session.add_all([
    User(name='alex',group_id=1),
    User(name='alex2',group_id=1),
    User(name='cc',group_id=2)
 ])

session.commit()
'''
#无虚拟关系的查询方法
ret = session.query(User.name,Group.caption).join(Group,isouter=True).all()
print(ret)
print "---------------------------------------------------------------"
#查询user表中所有数据
sql=session.query(User).join(Group,isouter=True)
print(sql)
print "---------------------------------------------------------------"
sql_all =session.query(User).join(Group,isouter=True).all()
print(sql_all)
print "---------------------------------------------------------------"

#需要虚拟关系的查询（即需要存在relationship）
#正向查询
ret = session.query(User).all()
for obj in ret:
#    #obj 代指user表的每一行数据
#    #obj.group 代指group对象
    print(obj.uid, obj.name, obj.group_id, obj.group, obj.group.gid, obj.group.caption)

print "---------------------------------------------------------------"

#反向查询原始方式
#查询用户组表中属于DBA组的用户名
ret=session.query(User.name,Group.caption).join(Group,isouter=True).filter(Group.caption=='DBA').all()
print(ret)
print "---------------------------------------------------------------"
#虚拟关系反向查询方式
#反向查询
#group中得到一个对象
obj=session.query(Group).filter(Group.caption=='DBA').first()
print(obj.gid)
print(obj.caption)
#连接到虚拟关系中backref设定的mygroup
print(obj.mygroup)

Base.metadata.drop_all(engine)
session.commit()