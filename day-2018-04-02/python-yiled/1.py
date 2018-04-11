def fab(max):

    n,a,b = 0,0,1
    while n<max:
        print(b)
        #先计算等式的右边，再去赋值给左边
        a,b=b,a+b
        n=n+1

fab(5)
"""
函数可生成一串数列，因为fab函数返回是None,但是其它函数无法获得该串数列。复用性较差......
"""