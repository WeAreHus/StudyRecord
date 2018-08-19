def fab(max):
    n,a,b=0,0,1
    L = []
    while n<max:
        L.append(b)
        a,b=b,a+b
        n=n+1
    return L

for n in fab(5):
    print(n)
"""
通过建立一个空list把迭代生成的数据元素存入在里面，这样这些数据就可以被复用在其他的函数里面
但是缺点是所有的数据都在list里面，这样会消耗大量的内存
"""