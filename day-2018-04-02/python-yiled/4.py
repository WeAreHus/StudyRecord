class abc(object):
    def __init__(self):
        self.a,self.b = 0,1 #初始化a,b

    def __iter__(self):
        return self #实例本身就是迭代对象，故返回自己

    def __next__(self):
        self.a ,self.b = self.b ,self.a+self.b #计算下一个值
        if self.a>10:
            raise StopIteration() #通过StopIteration来退出循环
        return self.a  #返回下一个值

for x in abc():
    print(x)

"""
迭代器走完一轮，抛出异常后，再次调用会先进行__iter__(),再进行__next__()。
"""