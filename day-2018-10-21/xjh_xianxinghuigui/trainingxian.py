# -*- coding: utf-8 -*-
# 预测LebronJames近三个赛季出手次数和得分之间的关系
import tensorflow as tf
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# 读取数据
train = pd.read_csv("/home/xiang/mygit/学习记录和随笔/AI/james.csv")
# 定义参数
train = train[train['shoot'] < 12000]
train_X = train['shoot'].values.reshape(-1,1)
train_Y = train['score'].values.reshape(-1,1)
n_samples = train_X.shape[0]

#学习率
learning_rate = 2
#训练次数
training_eppchs = 1000
#设置多少次显示一次
display_step = 50
# 定义X,Y占位符
X = tf.placeholder(tf.float32)
Y = tf.placeholder(tf.float32)
# 使用Variable定义学习参数
W = tf.Variable(np.random.randn(), name="weight", dtype=tf.float32)
b = tf.Variable(np.random.randn(), name="bias", dtype=tf.float32)
# 构建正向传播结构
pred = tf.add(tf.multiply(W, X), b)
# 损失函数
cost = tf.reduce_sum(tf.pow(pred-Y, 2))/(2*n_samples)
# 使用梯度下降优化器
optimizer = tf.train.AdamOptimizer(learning_rate).minimize(cost)
# 激活init
init = tf.global_variables_initializer()
# 启动session,初始化变量
with tf.Session() as sess:
    sess.run(init)
# 启动循环开始训练
    for epoch in range(training_eppchs):
        for (x, y) in zip(train_X, train_Y):
            sess.run(optimizer,feed_dict={X:x, Y:y})
# 显示训练中的详细信息
        if (epoch + 1) % display_step == 0:
            c = sess.run(cost, feed_dict={X:train_X, Y:train_Y})
            print("Epoch:", '%04d' % (epoch+1), "cost=", "{:.3f}".format(c), "W=", sess.run(W), "b=", sess.run(b))
    print("Optimization Finished!")
    training_cost = sess.run(cost, feed_dict={X:train_X, Y:train_Y})
    print("Training cost=", training_cost, "W=", sess.run(W), "b=", sess.run(b),'\n')
# 展示训练结果
    plt.plot(train_X, train_Y, 'ro', label="Original data")
    plt.plot(train_X, sess.run(W) * train_X + sess.run(b), label="Fitted line")
    plt.legend()
    plt.show()