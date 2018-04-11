def abc():
    a,b = 0,1
    while 1:
        a,b = b,a+b
        yield a

for x in abc():
    if x<10:
        print(x)
    else:
        break
"""
通过yield的作用，把一个函数变成了generator，并且函数返回一个iterable对象。
在for循环执行时，每次循环都会执行abc()函数的内部代码，执行到yield a时，abc()函数就返回一个迭代值，
下次迭代时，代码从yield b的下一条语句继续执行，而函数的本地变量看起来和上次中断执行前是完全一样的，
于是函数继续执行，直到再次遇见yield。
"""
