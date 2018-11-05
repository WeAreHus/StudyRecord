#-*-coding:utf-8-*-
import tensorflow as tf
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd

# 从CSV文件中读取数据，并返回2个数组。分别是自变量x和因变量y。方便TF计算模型。
def zc_read_csv():
    zc_dataframe = pd.read_csv('/home/xiang/mygit/学习记录和随笔/AI/james.csv')
    x = []
    y = []
    for zc_index in zc_dataframe.index:
        zc_row = zc_dataframe.loc[zc_index]
        x.append(zc_row["shoot"])
        y.append(zc_row["score"])
    return (x,y)

x, y = zc_read_csv()

# 获得画图对象。
fig = plt.figure()
fig.set_size_inches(10, 4)   # 整个绘图区域的宽度10和高度4
ax = fig.add_subplot(1, 2, 1)  # 整个绘图区分成一行两列，当前图是第一个。
# 画出原始数据的散点图。
ax.set_title("LeBornJames")
ax.set_xlabel("shoot")
ax.set_ylabel("score")
ax.scatter(x, y)
plt.show()
