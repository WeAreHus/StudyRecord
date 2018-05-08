# MySQL操作小结

[TOC]

---
## MySQL入门

### 安装MySQL
1.安装前先更新软件包列表
```
sudo apt updae
```
2.在Ubuntu 16.04 上安装MySQL
```
sudo apt-get install mysql-server mysql-client
```
3.在安装过程中需要你输入MySQL 管理员用户(root)密码
4.运行MySQL初始化安全脚本
```
sudo mysql_secure_installation
```
5.根据提示信息设置
mysql_secure_installation脚本设置的东西：更改root密码、移除MySQL的匿名用户、禁止root远程登录、删除test数据库。使用上面的这些选项可以提高MySQL的安全。

---
### MySQL数据库基本入门
1.使用root用户登录
```
mysql -u root -p
```
2.输入root密码：

输入root密码

3.创建MySQL数据库和用户
```sql
mysql> create database text;
```
上面命令创建了一个名为text的数据库

4.创建用户，并使用text数据库

增加用户：

（注意：和上面不同，下面的因为是MYSQL环境中的命令，所以后面都带分号作为命令结束符） 

格式：grant select on 数据库.* to 用户名@登录主机 identified by “密码”
```sql
mysql> grant all on text.* to 'user' identified by 'test1234';
```
创建了用户 user 密码为：test1234

5.使用新用户登录

我们现在退出root用户：
```sql
mysql> exit;
```
```
mysql -u user -p text
```
使用新用户登录，使用了名为text数据库
6.创建表
```sql
mysql> CREATE TABLE user (id INT, 
		name VARCHAR(20), 
		email VARCHAR(20)
		);
```
7.插入记录
```sql
mysql> INSERT INTO user (id,name,email) VALUES(1,"bar","bar@gmail.com");
mysql> INSERT INTO user (id,name,email) VALUES(2,"foo","foo@163.com");
mysql> INSERT INTO user (id,name,email) VALUES(3,"cat","cat@gmail.com");
```
8.简单查询
```sql
mysql> SELECT * FROM user;
```
---
## 更为详细的教程

---
### 查看数据库与数据：SHOW
```sql
show databases;
```
此语句将展示出所有数据库名
```sql
show tables;
```
此语句将展示出同一数据库下所有的数据表

---
### 创建数据表：CREATE
创建MySQL数据表需要以下信息：
- 表名
- 表字段名
- 定义每个表字段

**语法**

以下为创建MySQL数据表的SQL通用语法：
```sql
CREATE TABLE table_name (column_name column_type);
```
**实例**

以下例子中我们将在 text 数据库中创建数据表student：
```sql
CREATE TABLE IF NOT EXISTS student(
   id INT UNSIGNED AUTO_INCREMENT,
   name VARCHAR(20) NOT NULL,
   age INT NOT NULL,
   class INT,
   PRIMARY KEY ( id )
)ENGINE=InnoDB DEFAULT CHARSET=utf8;
```
实例解析：
- 如果你不想字段为 NULL 可以设置字段的属性为 NOT NULL， 在操作数据库时如果输入该字段的数据为NULL ，就会报错。
- AUTO_INCREMENT定义列为自增的属性，一般用于主键，数值会自动加1。
- PRIMARY KEY关键字用于定义列为主键。 您可以使用多列来定义主键，列间以逗号分隔。
- ENGINE 设置存储引擎，CHARSET 设置编码。

---
### 查看表结构：DESC
```sql
desc table_name;
```
或者
```
SHOW COLUMNS FROM table_name;
```
---
### 查看建表语句
```sql
show create table study_record;
```
---
### 删除数据表与数据库：DROP
```sql
DROP TABLE table_name ;
```
```sql
DROP DATABASE database_name;
```
---
### 选择数据库：USE
```sql
mysql> use database_name;
```
---
### 插入数据：INSERT
MySQL 表中使用 INSERT INTO SQL语句来插入数据。

**语法**

以下为向MySQL数据表插入数据通用的 INSERT INTO SQL语法：
```sql
INSERT INTO table_name ( field1, field2,...fieldN )
                       VALUES
                       ( value1, value2,...valueN );
```
如果数据是字符型，必须使用单引号或者双引号，如："value"

**实例**

以下我们将使用 SQL INSERT INTO 语句向 MySQL 数据表 student 插入数据:
```sql
mysql> INSERT INTO student 
    -> (id, name, age, class)
    -> VALUES
    -> (1, "Tom", 18, 1604);

mysql> INSERT INTO student 
    -> (id, name, age, class)
    -> VALUES
    -> (2, "Jarry", 17, 1605);

mysql> INSERT INTO student 
    -> (id, name, age, class)
    -> VALUES
    -> (3, "Judy", 19, 1606);
```
---
### 查询数据：SELECT

**语法**

以下为在MySQL数据库中查询数据通用的 SELECT 语法：
```sql
SELECT column_name,column_name
FROM table_name
[WHERE Clause]
[LIMIT N][ OFFSET M]
```
- 查询语句中你可以使用一个或者多个表，表之间使用逗号(,)分割，并使用WHERE语句来设定查询条件。
- SELECT 命令可以读取一条或者多条记录。
- 你可以使用星号（*）来代替其他字段，SELECT语句会返回表的所有字段数据
- 你可以使用 WHERE 语句来包含任何条件。
- 你可以使用 LIMIT 属性来设定返回的记录数。
- 你可以通过OFFSET指定SELECT语句开始查询的数据偏移量。默认情况下偏移量为0。
```sql
mysql> select * from student;
```
结果如下:
```
mysql> SELECT * from student;
+----+-------+-----+-------+
| id | name  | age | class |
+----+-------+-----+-------+
|  1 | Tom   |  18 |  1604 |
|  2 | Jarry |  17 |  1605 |
|  3 | Judy  |  19 |  1606 |
+----+-------+-----+-------+
```
---
### 控制指令：WHERE
我们知道从 MySQL 表中使用 SQL SELECT 语句来读取数据。

如需有条件地从表中选取数据，可将 WHERE 子句添加到 SELECT 语句中，在此，WHERE相当于编程语言中的if语句。

**语法**

以下是 SQL SELECT 语句使用 WHERE 子句从数据表中读取数据的通用语法：
```sql
SELECT field1, field2,...fieldN FROM table_name1, table_name2...
[WHERE condition1 [AND [OR]] condition2.....
```
- 查询语句中你可以使用一个或者多个表，表之间使用逗号, 分割，并使用WHERE语句来设定查询条件。
- 你可以在 WHERE 子句中指定任何条件。
- 你可以使用 AND 或者 OR 指定一个或多个条件。
- WHERE 子句也可以运用于 SQL 的 DELETE 或者 UPDATE 命令。
- WHERE 子句类似于程序语言中的 if 条件，根据 MySQL 表中的字段值来读取指定的数据。
```sql
SELECT * from student WHERE id = 1;
```
结果：
```
mysql> SELECT * from student WHERE id = 1;
+----+------+-----+-------+
| id | name | age | class |
+----+------+-----+-------+
|  1 | Tom  |  18 |  1604 |
+----+------+-----+-------+
```
---
### 更新指令：UPDATE
如果我们需要修改或更新 MySQL 中的数据，我们可以使用 SQL UPDATE 命令来操作。

**语法**

以下是 UPDATE 命令修改 MySQL 数据表数据的通用 SQL 语法：
```sql
UPDATE table_name SET field1=new-value1, field2=new-value2 [WHERE Clause]
```
- 你可以同时更新一个或多个字段。
- 你可以在 WHERE 子句中指定任何条件。
- 你可以在一个单独表中同时更新数据。

**实例**

以下实例将更新数据表中 id 为 3 的 age 字段值：
```
mysql> UPDATE student SET age = 20 WHERE id = 3;
Query OK, 1 row affected (0.01 sec)
Rows matched: 1  Changed: 1  Warnings: 0
```
我们使用SELECT看看结果：
```
mysql> select * from student;
+----+-------+-----+-------+
| id | name  | age | class |
+----+-------+-----+-------+
|  1 | Tom   |  18 |  1604 |
|  2 | Jarry |  17 |  1605 |
|  3 | Judy  |  20 |  1606 |
+----+-------+-----+-------+
```
从结果上看我们成功修改了id 为3的年龄

---
### 删除指令：DELETE
你可以使用 SQL 的 DELETE FROM 命令来删除 MySQL 数据表中的记录。

**语法**

以下是 SQL DELETE 语句从 MySQL 数据表中删除数据的通用语法：
```sql
DELETE FROM table_name [WHERE Clause]
```
- 如果没有指定 WHERE 子句，MySQL 表中的**所有记录**将被删除。
- 你可以在 WHERE 子句中指定任何条件
- 您可以在单个表中一次性删除记录。

**实例**

我们现在把Judy从student表中删除：
```sql
mysql> DELETE FROM student WHERE name = 'Judy';
```
现在来看看结果:
```
mysql> select * from student;
+----+-------+-----+-------+
| id | name  | age | class |
+----+-------+-----+-------+
|  1 | Tom   |  18 |  1604 |
|  2 | Jarry |  17 |  1605 |
+----+-------+-----+-------+
```
---
### LIKE子句
我们知道在 MySQL 中使用 SQL SELECT 命令来读取数据， 同时我们可以在 SELECT 语句中使用 WHERE 子句来获取指定的记录。

WHERE 子句中可以使用等号 = 来设定获取数据的条件，但是有时候我们需要获取 name 字段含有 "COM" 字符的所有记录，这时我们就需要在 WHERE 子句中使用 SQL LIKE 子句。

SQL LIKE 子句中使用百分号 %字符来表示任意字符，类似于UNIX或正则表达式中的星号 *。

如果没有使用百分号 %, LIKE 子句与等号 = 的效果是一样的。

**语法**

以下是 SQL SELECT 语句使用 LIKE 子句从数据表中读取数据的通用语法：

```sql
SELECT field1, field2,...fieldN 
FROM table_name
WHERE field1 LIKE condition1 [AND [OR]] filed2 = 'somevalue'
```
- 你可以在 WHERE 子句中指定任何条件。
- 你可以在 WHERE 子句中使用LIKE子句。
- 你可以使用LIKE子句代替等号 =。
- LIKE 通常与 % 一同使用，类似于一个元字符的搜索。
- 你可以使用 AND 或者 OR 指定一个或多个条件。
- 你可以在 DELETE 或 UPDATE 命令中使用 WHERE...LIKE 子句来指定条件。

**实例**

为了表现得更直观，我们向student表中多插入几行数据：
```
mysql> select *  from student;
+----+---------+-----+-------+
| id | name    | age | class |
+----+---------+-----+-------+
|  1 | Tom     |  18 |  1604 |
|  2 | Jarry   |  17 |  1605 |
|  3 | Azad    |  19 |  1606 |
|  4 | Andrzej |  19 |  1606 |
|  5 | Abu     |  19 |  1606 |
+----+---------+-----+-------+

```
现在我们使用SELECT配合LIKE来查询所有name首字母为A的学生；
```sql
mysql> SELECT * from student WHERE name LIKE 'A%';
```
返回结果：
```
mysql> SELECT * from student WHERE name LIKE 'A%';
+----+---------+-----+-------+
| id | name    | age | class |
+----+---------+-----+-------+
|  4 | Azad    |  19 |  1606 |
|  5 | Andrzej |  19 |  1606 |
|  6 | Abu     |  19 |  1606 |
+----+---------+-----+-------+
```
---
### 正则表达式
在前面的章节我们已经了解到MySQL可以通过 LIKE ...% 来进行模糊匹配。

MySQL 同样也支持其他正则表达式的匹配， MySQL中使用 REGEXP 操作符来进行正则表达式匹配。

如果您了解PHP或Perl，那么操作起来就非常简单，因为MySQL的正则表达式匹配与这些脚本的类似。

下表中的正则模式可应用于 REGEXP 操作符中。

| 模式 | 描述 |
| :-: | - |
| ^ | 	匹配输入字符串的开始位置。如果设置了 RegExp 对象的 Multiline 属性，^ 也匹配 '\n' 或 '\r' 之后的位置。  |
| $ | 匹配输入字符串的结束位置。如果设置了RegExp 对象的 Multiline 属性，也匹配 '\n' 或 '\r' 之前的位置。|
| . | 匹配除 "\n" 之外的任何单个字符。要匹配包括 '\n' 在内的任何字符，请使用象 '[.\n]' 的模式。|
| [...] |字符集合。匹配所包含的任意一个字符。例如， '[abc]' 可以匹配 "plain" 中的 'a'。|
| [^...] |负值字符集合。匹配未包含的任意字符。例如， '[^abc]' 可以匹配 "plain" 中的'p'。|
|* |匹配前面的子表达式零次或多次。例如，zo* 能匹配 "z" 以及 "zoo"。* 等价于{0,}。|
| + |匹配前面的子表达式一次或多次。例如，'zo+' 能匹配 "zo" 以及 "zoo"，但不能匹配 "z"。+ 等价于 {1,}。|
|{n} | 	n 是一个非负整数。匹配确定的 n 次。例如，'o{2}' 不能匹配 "Bob" 中的 'o'，但是能匹配 "food" 中的两个 o。|
| {n,m} | m 和 n 均为非负整数，其中n <= m。最少匹配 n 次且最多匹配 m 次。|

**实例**

了解以上的正则需求后，我们就可以根据自己的需求来编写带有正则表达式的SQL语句。以下我们将列出几个小实例(表名：person_tbl )来加深我们的理解：

查找name字段中以'J'为开头的所有数据：
```sql
mysql> SELECT name FROM student WHERE name REGEXP '^J';
```
查找name字段中以'y'为结尾的所有数据：
```sql
mysql> SELECT name FROM studnet WHERE name REGEXP 'y$';
```
查找name字段中包含'a'字符串的所有数据：
```sql
mysql> SELECT name FROM student WHERE name REGEXP 'a';
```
查找name字段中以元音字符开头或以'u'字符串结尾的所有数据：
```sql
mysql> SELECT name FROM student WHERE name REGEXP '^[aeiou]|u$';
```

---
### 排序：ORDER BY
我们知道从 MySQL 表中使用 SQL SELECT 语句来读取数据。

如果我们需要对读取的数据进行排序，我们就可以使用 MySQL 的 ORDER BY 子句来设定你想按哪个字段哪种方式来进行排序，再返回搜索结果。

**语法**

以下是 SQL SELECT 语句使用 ORDER BY 子句将查询数据排序后再返回数据：
```sql
SELECT field1, field2,...fieldN table_name1, table_name2...
ORDER BY field1, [field2...] [ASC [DESC]]
```
- 你可以使用任何字段来作为排序的条件，从而返回排序后的查询结果。
- 你可以设定多个字段来排序。
- 你可以使用 ASC 或 DESC 关键字来设置查询结果是按升序或降序排列。 默认情况下，它是按升序排列。
- 你可以添加 WHERE...LIKE 子句来设置条件。

**实例**

以下将在 SQL SELECT 语句中使用 ORDER BY 子句来读取MySQL 数据表 score 中的数据：

尝试以下实例，结果将按升序及降序排列。

升序：
```
mysql> select * from score order by score ASC;
+----+------+---------+-------+
| id | name | class   | score |
+----+------+---------+-------+
|  2 | Tom  | English |    45 |
|  3 | Azad | math    |    90 |
|  1 | Tom  | math    |    97 |
|  4 | Abu  | Chinese |    99 |
+----+------+---------+-------+
```
降序：
```
mysql> select * from score order by score DESC;
+----+------+---------+-------+
| id | name | class   | score |
+----+------+---------+-------+
|  4 | Abu  | Chinese |    99 |
|  1 | Tom  | math    |    97 |
|  3 | Azad | math    |    90 |
|  2 | Tom  | English |    45 |
+----+------+---------+-------+
```
---
### UNION操作符
MySQL UNION 操作符用于连接两个以上的 SELECT 语句的结果组合到一个结果集合中。多个 SELECT 语句会删除重复的数据。

**语法**

MySQL UNION 操作符语法格式：
```sql
SELECT expression1, expression2, ... expression_n
FROM tables
[WHERE conditions]
UNION [ALL | DISTINCT]
SELECT expression1, expression2, ... expression_n
FROM tables
[WHERE conditions];
```
- expression1, expression2, ... expression_n: 要检索的列。
- tables: 要检索的数据表。
- WHERE conditions: 可选， 检索条件。
- DISTINCT: 可选，删除结果集中重复的数据。默认情况下 UNION 操作符已经删除了重复数据，所以 DISTINCT 修饰符对结果没啥影响。
- ALL: 可选，返回所有结果集，包含重复数据。

**实例**

score表：
```
mysql> select * from score;
+----+------+---------+-------+
| id | name | class   | score |
+----+------+---------+-------+
|  1 | Tom  | math    |    97 |
|  2 | Tom  | English |    45 |
|  3 | Azad | math    |    90 |
|  4 | Abu  | Chinese |    99 |
+----+------+---------+-------+
```
student表：
```
mysql> select * from student;
+----+---------+-----+-------+
| id | name    | age | class |
+----+---------+-----+-------+
|  1 | Tom     |  18 |  1604 |
|  2 | Jarry   |  17 |  1605 |
|  4 | Azad    |  19 |  1606 |
|  5 | Andrzej |  19 |  1606 |
|  6 | Abu     |  19 |  1606 |
+----+---------+-----+-------+
```
下面的 SQL 语句从 "student" 和 "score" 表中选取所有不同的name（只有不同的值）：
```sql
mysql> select name from student
    -> union
    -> select name from score
    -> order by name;
```
结果：
```
+---------+
| name    |
+---------+
| Abu     |
| Andrzej |
| Azad    |
| Jarry   |
| Tom     |
+---------+
```
#### UNION ALL 操作符
下面的 SQL 语句使用 UNION ALL 从 "student" 和 "score" 表中选取所有的name（也有重复的值）：
```sql
mysql> select name from student
    -> union all
    -> select name from score
    -> order by name;
```
结果：
```
+---------+
| name    |
+---------+
| Abu     |
| Abu     |
| Andrzej |
| Azad    |
| Azad    |
| Jarry   |
| Tom     |
| Tom     |
| Tom     |
+---------+
```
---
### 分组：GROUP BY(暂空)
GROUP BY 语句根据一个或多个列对结果集进行分组。

在分组的列上我们可以使用 COUNT, SUM, AVG,等函数。

**语法**
```sql
SELECT column_name, function(column_name)
FROM table_name
WHERE column_name operator value
GROUP BY column_name;
```
---
### 数据表链接：JOIN
在前几章节中，我们已经学会了如何在一张表中读取数据，这是相对简单的，但是在真正的应用中经常需要从多个数据表中读取数据。

本章节我们将向大家介绍如何使用 MySQL 的 JOIN 在两个或多个表中查询数据。

你可以在 SELECT, UPDATE 和 DELETE 语句中使用 Mysql 的 JOIN 来联合多表查询。

JOIN 按照功能大致分为如下三类：

- INNER JOIN（内连接,或等值连接）：获取两个表中字段匹配关系的记录。
- LEFT JOIN（左连接）：获取左表所有记录，即使右表没有对应匹配的记录。
- RIGHT JOIN（右连接）： 与 LEFT JOIN 相反，用于获取右表所有记录，即使左表没有对应匹配的记录。
![enter image description here](https://images2017.cnblogs.com/blog/1035967/201709/1035967-20170907174926054-907920122.jpg)
**实例**

接下来我们就使用MySQL的INNER JOIN(也可以省略 INNER 使用 JOIN，效果一样)来连接以上两张表来读取score表中所有name字段在student表对应的age和class字段值：
```sql
mysql> SELECT a.id, a.name, a.class, a.score, b.age, b.class FROM score a
    -> JOIN
    -> students b
    -> on
    -> a.id = b.id;
```
等价于：
```sql
mysql> SELECT a.id, a.name, a.class, a.score, b.age, b.class FROM score a, students b
    -> WHERE a.id = b.id;
```
结果：
```
+----+------+---------+-------+-----+-------+
| id | name | class   | score | age | class |
+----+------+---------+-------+-----+-------+
|  1 | Tom  | math    |    97 |  18 |  1604 |
|  2 | Tom  | English |    45 |  17 |  1605 |
|  3 | Azad | math    |    90 |  19 |  1606 |
|  4 | Abu  | Chinese |    99 |  19 |  1606 |
+----+------+---------+-------+-----+-------+
```
#### LEFT JOIN和RIGHT JOIN
MySQL left join 与 join 有所不同。 MySQL LEFT JOIN 会读取左边数据表的全部数据，即便右边表无对应数据。

同样的，RIGHT JOIN会读取右边数据表全部数据，即使左边表无对应数据。

**实例**
```sql
mysql> SELECT a.id, a.name, a.class, a.score, b.age, b.class FROM score a
    -> RIGHT JOIN
    -> students b
    -> on
    -> a.id = b.id;
+------+------+---------+-------+-----+-------+
| id   | name | class   | score | age | class |
+------+------+---------+-------+-----+-------+
|    1 | Tom  | math    |    97 |  18 |  1604 |
|    2 | Tom  | English |    45 |  17 |  1605 |
|    3 | Azad | math    |    90 |  19 |  1606 |
|    4 | Abu  | Chinese |    99 |  19 |  1606 |
| NULL | NULL | NULL    |  NULL |  19 |  1606 |
+------+------+---------+-------+-----+-------+
```

---
### 修改数据表：ALTER

当我们需要修改数据表名或者修改数据表字段时，就需要使用到MySQL ALTER命令。

我们用前面的score表来演示一下：

我们先来看看score表的字段属性：
```
mysql> desc score;
+-------+-------------+------+-----+---------+----------------+
| Field | Type        | Null | Key | Default | Extra          |
+-------+-------------+------+-----+---------+----------------+
| id    | int(11)     | NO   | PRI | NULL    | auto_increment |
| name  | varchar(20) | NO   |     | NULL    |                |
| class | varchar(20) | NO   |     | NULL    |                |
| score | int(11)     | NO   |     | NULL    |                |
+-------+-------------+------+-----+---------+----------------+
```

#### 修改字段类型及名称
如果需要修改字段类型及名称, 你可以在ALTER命令中使用 MODIFY 或 CHANGE 子句 。

例如，把字段 name 的类型从 VARCHAR(20) 改为 VARCHAR(10)，可以执行以下命令:
```sql
mysql> ALTER TABLE score MODIFY name CHAR(10);
```
使用 CHANGE 子句, 语法有很大的不同。 在 CHANGE 关键字之后，紧跟着的是你要修改的字段名，然后指定新字段名及类型。尝试如下实例：
```sql
mysql> ALTER TABLE score CHANGE class subject varchar(20);
```
```sql
mysql> ALTER TABLE score CHANGE subject subject varchar(10);
```

#### 删除，添加或修改表字段

MySQL 中使用 ADD 子句来向数据表中添加列，如下实例在表 score 中添加 major 字段，并定义数据类型:
```sql
mysql> ALTER TABLE score ADD major varchar(20);
```
执行以上命令后，major 字段会自动添加到数据表字段的末尾。
```
mysql> desc score;
+---------+-------------+------+-----+---------+----------------+
| Field   | Type        | Null | Key | Default | Extra          |
+---------+-------------+------+-----+---------+----------------+
| id      | int(11)     | NO   | PRI | NULL    | auto_increment |
| name    | char(10)    | YES  |     | NULL    |                |
| subject | varchar(20) | YES  |     | NULL    |                |
| score   | int(11)     | NO   |     | NULL    |                |
| major   | varchar(20) | YES  |     | NULL    |                |
+---------+-------------+------+-----+---------+----------------+
```
如果你需要指定新增字段的位置，可以使用MySQL提供的关键字 FIRST (设定位第一列)， AFTER 字段名（设定位于某个字段之后）。

如下命令使用了 ALTER 命令及 DROP 子句来删除以上创建表的 i 字段：
```sql
mysql> ALTER TABLE score DROP major;
```
如果数据表中只剩余一个字段则无法使用DROP来删除字段。

尝试以下 ALTER TABLE 语句, 在执行成功后，使用 SHOW COLUMNS 查看表结构的变化：
```sql
ALTER TABLE score DROP major;
ALTER TABLE score ADD major varchar(20) FIRST;
ALTER TABLE score DROP major;
ALTER TABLE score ADD major varchar(20) AFTER name;
```
```
mysql> desc score;
+---------+-------------+------+-----+---------+----------------+
| Field   | Type        | Null | Key | Default | Extra          |
+---------+-------------+------+-----+---------+----------------+
| id      | int(11)     | NO   | PRI | NULL    | auto_increment |
| name    | char(10)    | YES  |     | NULL    |                |
| major   | varchar(20) | YES  |     | NULL    |                |
| subject | varchar(20) | YES  |     | NULL    |                |
| score   | int(11)     | NO   |     | NULL    |                |
+---------+-------------+------+-----+---------+----------------+
```
#### ALTER TABLE 对 Null 值和默认值的影响
当你修改字段时，你可以指定是否包含值或者是否设置默认值。

以下实例，指定字段 major 为 NOT NULL 且默认值为100 。
```
mysql> ALTER TABLE score MODIFY major varchar(20) NOT NULL DEFAULT 'NO';
```

#### 修改字段默认值
你可以使用 ALTER 来修改字段的默认值，尝试以下实例：
```
mysql> ALTER TABLE score ALTER major SET DEFAULT 'OK';
```
你也可以使用 ALTER 命令及 DROP子句来删除字段的默认值，如下实例：
```
mysql> ALTER TABLE score ALTER major DROP DEFAULT;
```
修改数据表类型，可以使用 ALTER 命令及 TYPE 子句来完成。尝试以下实例，我们将表 score 的类型修改为 MYISAM ：

#### 修改表名
如果需要修改数据表的名称，可以在 ALTER TABLE 语句中使用 RENAME 子句来实现。

尝试以下实例将数据表 score重命名为 student_score：
```
mysql> ALTER TABLE score RENAME TO student_score;
```
ALTER 命令还可以用来创建及删除MySQL数据表的索引，该功能我们会在接下来的章节中介绍。

---
### 索引：INDEX
MySQL索引的建立对于MySQL的高效运行是很重要的，索引可以大大提高MySQL的检索速度。

索引分单列索引和组合索引。单列索引，即一个索引只包含单个列，一个表可以有多个单列索引，但这不是组合索引。组合索引，即一个索引包含多个列。

创建索引时，你需要确保该索引是应用在	SQL 查询语句的条件(一般作为 WHERE 子句的条件)。

实际上，索引也是一张表，该表保存了主键与索引字段，并指向实体表的记录。

上面都在说使用索引的好处，但过多的使用索引将会造成滥用。因此索引也会有它的缺点：虽然索引大大提高了查询速度，同时却会降低更新表的速度，如对表进行INSERT、UPDATE和DELETE。因为更新表时，MySQL不仅要保存数据，还要保存一下索引文件。

建立索引会占用磁盘空间的索引文件。

#### 普通索引

**创建索引**

这是最基本的索引，它没有任何限制。它有以下几种创建方式：
```sql
CREATE INDEX indexName ON mytable(username(length)); 
```
如果是CHAR，VARCHAR类型，length可以小于字段实际长度；如果是BLOB和TEXT类型，必须指定 length。

**修改表结构(添加索引)**
```sql
ALTER table tableName ADD INDEX indexName(columnName)
```
**创建表的时候直接指定**
```sql
CREATE TABLE mytable(  
 
ID INT NOT NULL,   
 
username VARCHAR(16) NOT NULL,  
 
INDEX [indexName] (username(length))  
 
);  
```
**删除索引的语法**
```sql
DROP INDEX [indexName] ON mytable; 
```
#### 唯一索引
它与前面的普通索引类似，不同的就是：索引列的值必须唯一，但允许有空值。如果是组合索引，则列值的组合必须唯一。它有以下几种创建方式：

**创建索引**
```sql
CREATE UNIQUE INDEX indexName ON mytable(username(length)) 
```
**修改表结构**
```sql
ALTER table mytable ADD UNIQUE [indexName] (username(length))
```
**创建表的时候直接指定**
```sql
CREATE TABLE mytable(  
 
ID INT NOT NULL,   
 
username VARCHAR(16) NOT NULL,  
 
UNIQUE [indexName] (username(length))  
 
);
```
#### 使用ALTER 命令添加和删除索引
有四种方式来添加数据表的索引：

- ALTER TABLE tbl_name ADD PRIMARY KEY (column_list): 该语句添加一个主键，这意味着索引值必须是唯一的，且不能为NULL。
- ALTER TABLE tbl_name ADD UNIQUE index_name (column_list): 这条语句创建索引的值必须是唯一的（除了NULL外，NULL可能会出现多次）。
- ALTER TABLE tbl_name ADD INDEX index_name (column_list): 添加普通索引，索引值可出现多次。
- ALTER TABLE tbl_name ADD FULLTEXT index_name (column_list):该语句指定了索引为 FULLTEXT ，用于全文索引。

以下实例为在表中添加索引。
```sql
mysql> ALTER TABLE testalter_tbl ADD INDEX (c);
```
你还可以在 ALTER 命令中使用 DROP 子句来删除索引。尝试以下实例删除索引:
```sql
mysql> ALTER TABLE testalter_tbl DROP INDEX c;
```

#### 使用 ALTER 命令添加和删除主键
主键只能作用于一个列上，添加主键索引时，你需要确保该主键默认不为空（NOT NULL）。实例如下：
```sql
mysql> ALTER TABLE testalter_tbl MODIFY i INT NOT NULL;
mysql> ALTER TABLE testalter_tbl ADD PRIMARY KEY (i);
```
你也可以使用 ALTER 命令删除主键：
```sql
mysql> ALTER TABLE testalter_tbl DROP PRIMARY KEY;
```
删除主键时只需指定PRIMARY KEY，但在删除索引时，你必须知道索引名。

#### 显示索引信息
你可以使用 SHOW INDEX 命令来列出表中的相关的索引信息。可以通过添加 \G 来格式化输出信息。

尝试以下实例:
```sql
mysql> SHOW INDEX FROM table_name; \G
........
```

---
### 事务

MySQL 事务主要用于处理操作量大，复杂度高的数据。比如说，在人员管理系统中，你删除一个人员，你即需要删除人员的基本资料，也要删除和该人员相关的信息，如信箱，文章等等，这样，这些数据库操作语句就构成一个事务！

- 在 MySQL 中只有使用了 Innodb 数据库引擎的数据库或表才支持事务。
- 事务处理可以用来维护数据库的完整性，保证成批的 SQL 语句要么全部执行，要么全部不执行。
- 事务用来管理 insert,update,delete 语句

**MYSQL 事务处理主要有两种方法：**

1、用 BEGIN, ROLLBACK, COMMIT来实现

- BEGIN 开始一个事务
- ROLLBACK 事务回滚
- COMMIT 事务确认

2、直接用 SET 来改变 MySQL 的自动提交模式:

- SET AUTOCOMMIT=0 禁止自动提交
- SET AUTOCOMMIT=1 开启自动提交

一般来说，事务是必须满足4个条件（ACID）：原子性（Atomicity，或称不可分割性）、一致性（Consistency）、隔离性（Isolation，又称独立性）、持久性（Durability）。

- 原子性：一个事务（transaction）中的所有操作，要么全部完成，要么全部不完成，不会结束在中间某个环节。事务在执行过程中发生错误，会被回滚（Rollback）到事务开始前的状态，就像这个事务从来没有执行过一样。

- 一致性：在事务开始之前和事务结束以后，数据库的完整性没有被破坏。这表示写入的资料必须完全符合所有的预设规则，这包含资料的精确度、串联性以及后续数据库可以自发性地完成预定的工作。

- 隔离性：数据库允许多个并发事务同时对其数据进行读写和修改的能力，隔离性可以防止多个事务并发执行时由于交叉执行而导致数据的不一致。事务隔离分为不同级别，包括读未提交（Read uncommitted）、读提交（read committed）、可重复读（repeatable read）和串行化（Serializable）。

- 持久性：事务处理结束后，对数据的修改就是永久的，即便系统故障也不会丢失。

*在 MySQL 命令行的默认设置下，事务都是自动提交的，即执行 SQL 语句后就会马上执行 COMMIT 操作。因此要显式地开启一个事务务须使用命令 BEGIN 或 START TRANSACTION，或者执行命令 SET AUTOCOMMIT=0，用来禁止使用当前会话的自动提交。*

**事务控制语句：**
- BEGIN或START TRANSACTION；显式地开启一个事务；

- COMMIT；也可以使用COMMIT WORK，不过二者是等价的。COMMIT会提交事务，并使已对数据库进行的所有修改称为永久性的；

- ROLLBACK；有可以使用ROLLBACK WORK，不过二者是等价的。回滚会结束用户的事务，并撤销正在进行的所有未提交的修改；

- SAVEPOINT identifier；SAVEPOINT允许在事务中创建一个保存点，一个事务中可以有多个SAVEPOINT；

- RELEASE SAVEPOINT identifier；删除一个事务的保存点，当没有指定的保存点时，执行该语句会抛出一个异常；

- ROLLBACK TO identifier；把事务回滚到标记点；

- SET TRANSACTION；用来设置事务的隔离级别。InnoDB存储引擎提供事务的隔离级别有READ UNCOMMITTED、READ COMMITTED、REPEATABLE READ和SERIALIZABLE。