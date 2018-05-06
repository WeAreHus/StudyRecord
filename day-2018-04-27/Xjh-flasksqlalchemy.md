# flask-sqlalchemy
----
###关于flask-sqlalchemy
flask-sqlalchemy是在sqlalchemy基础上封装了一层.
与普通SQLAlchemy相比,需要了解的是：  
1. SQLAlchemy 使您可以访问以下内容：  
* 来自sqlalchemy和的 所有功能和类sqlalchemy.orm
* 一个预先配置的被称为范围的会话 session
* 该 metadata
* 该 engine
* a SQLAlchemy.create_all()和SQLAlchemy.drop_all() 根据模型创建和删除表的方法。
* 一个Model基类，它是一个配置的声明基础。
2. 所述Model声明性基类的行为就像一个常规的Python类,但有一个query附加属性，该属性可以被用来查询模型。（Model和BaseQuery）
3. 您必须提交会话，但您不必在请求结束时将其删除，Flask-SQLAlchemy会为您执行此操作。
