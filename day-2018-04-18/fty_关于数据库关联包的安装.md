# 关于数据库关联包的安装
---
### 什么是MySQLdb?
MySQLdb 是用于Python链接Mysql数据库的接口，它实现了 Python 数据库 API 规范 V2.0，基于 MySQL C API 上建立的。

### 如何安装MySQLdb?
为了用DB-API编写MySQL脚本，必须确保已经安装了MySQL。复制以下代码，并执行：
```
import MySQLdb
```
如果执行后的输出结果如下所示，意味着你没有安装 MySQLdb 模块：
```
Traceback (most recent call last):
  File "test.py", line 3, in <module>
    import MySQLdb
ImportError: No module named MySQLdb
```
安装MySQLdb，请访问 http://sourceforge.net/projects/mysql-python ，(Linux平台可以访问：https://pypi.python.org/pypi/MySQL-python)从这里可选择适合您的平台的安装包，分为预编译的二进制文件和源代码安装包。

如果您选择二进制文件发行版本的话，安装过程基本安装提示即可完成。如果从源代码进行安装的话，则需要切换到MySQLdb发行版本的顶级目录，并键入下列命令:
```
$ gunzip MySQL-python-1.2.2.tar.gz
$ tar -xvf MySQL-python-1.2.2.tar
$ cd MySQL-python-1.2.2
$ python setup.py build
$ python setup.py install
```
**注意：请确保您有root权限来安装上述模块。**
---
### 如何安装pip？
下载文件

`wget https://bootstrap.pypa.io/get-pip.py --no-check-certificate`

执行安装

`python get-pip.py`

完成

---
### 如何安装SQLAlchemy?
使用pip安装：`pip install sqlalchemy`

使用easy_install安装：`easy_install sqlalchemy`

或者：

`http://pypi.douban.com/packages/source/S/SQLAlchemy/SQLAlchemy-0.9.3.tar.gz
tar -xzvf SQLAlchemy-0.9.3.tar.gz
cd SQLAlchemy-0.9.3 
sudo python setup.py install`
