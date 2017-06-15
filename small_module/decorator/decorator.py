#!/usr/bin/env python
# coding: utf-8


from functools import wraps

LINE = "*" * 50

# 1. 普通函数
def f1():
    print("function f1 is called.")
    print(LINE)

# 2. 作用域
global_str = "This is a global variable"
def f2():
    print("function f2 is called.")
    print("function f2 local var: \t", end="")
    print(locals())
    print("function f2 global var: \t", end="")
    print(globals())
    global_str = "global string is replaced."
    print("function f2 global var: \t", end="")
    print(globals())
    print(LINE)

# 3. 生存周期
def f3_1():
    print("function f3_1 is called.")
    x = 1
    try:
        print(x)
    except NameError as e:
        print(e)

def f3_2():
    print("function f3_2 is called.")
    try:
        print(x)
    except NameError as e:
        print(e)

# 4. 参数
def f4_1(x, y = 0):
    print(x - y)

def f4_2():
    print("function f4 is called.")
    f4_1(2, 1)
    f4_1(2)
    f4_1(y=2, x=1)
    print(LINE)

# 5. 函数是参数
def f5_1(x, y):
    return(x + y)

def f5_2(x, y):
    return(x - y)

def f5_3(func, x, y):
    return(func(x, y))

def f5_4():
    print("function f5 is called.")
    add = f5_3(f5_1, 1, 2)
    sub = f5_3(f5_2, 1, 2)
    print(add)
    print(sub)
    print(LINE)

# 6. 返回值是函数
def f6_1():
    def f6_inner():
        print("function f6_inner is called.")
    return f6_inner

def f6_2():
    foo = f6_1()
    foo()
    print(LINE)

# 7. 作用域内局部变量可被外部调用
def f7_1():
    x = 1
    def f7_inner():
        print("function f7_inner is called.")
        print(x)
    return f7_inner

def f7_2():
    print("function f7_2 is called.")
    foo = f7_1()
    print("call function f7_1.")
    foo()
    print(LINE)

# 8. [函数闭包] - 嵌套定义在非全局作用域里面的函数能够记住它在被定义的时候它所处的封闭命名空间
def f8_1(x):
    def f8_inner():
        print("function f8_inner is called.")
        print(x)
    return f8_inner

def f8_2():
    print("function f8 is called.")
    printer1 = f8_1(1)
    printer2 = f8_1(2)
    print("a function printer1 without param is called.")
    printer1()
    print("a function printer2 without param is called.")
    printer2()
    print(LINE)

# 9. 装饰器 - 一个闭包, 把一个函数当做参数然后返回一个替代版函数
def f9_1(func):
    def f9_inner():
        print("CAN DO sth. before call function.")
        ret = func()
    return f9_inner

def f9_2():
    print("function f9_2 is called.")
    return 1

def f9_3():
    print("function f9 is called.")
    print("call f9_2.")
    origin = f9_2
    origin()
    print("call decorated f9_2.")
    decorated = f9_1(f9_2)
    decorated()
    print(LINE)

# 10. 装饰器@
def f10_logger(func):
    def logger(*args, **kw):
        print("logger before call function!")
        return func(*args, **kw)
    return logger

def f10_1():
    print("function f10_1 is called.")

def f10_2():
    func = f10_logger(f10_1)
    func()

# means f10_3 = f10_logger(f10_1)
@f10_logger
def f10_3():
    f10_1()
    print(LINE)

# 11. 函数式带参数@
def f11_logger(p1, p2):
    def decorator(func):
        def logger(*args, **kw):
            print("logger before call function!")
            print("param is %s and %s." % (p1, p2))
            return func(*args, **kw)
        return logger
    return decorator

def f11_1():
    print("function f11_1 is called.")

@f11_logger("test1", "test2")
def f11_2():
    f11_1()
    print(LINE)

# 12. 装饰器@的类形式, 必须确保实现__call__()方法
class myDecorator(object):
    def __init__(self, p1, p2):
        print("inside myDecorator.__init__()")
        self.__p1 = p1
        self.__p2 = p2

    def __call__(self, func):
        def wrapped(*args, **kwargs):
            print("inside myDecorator.__call__()")
            print(self.__p1, self.__p2)
        return wrapped

@myDecorator("class_test1", "class_test2")
def f12_1():
    print("function f12_1 is called.")

def f12_2():
    print("function f12_2 is called.")
    print("call function f12_1.")
    f12_1()


if __name__ == "__main__":
    f1()
    f2()
    f3_1()
    f3_2()
    f4_2()
    f5_4()
    f6_2()
    f7_2()
    f8_2()
    f9_3()
    f10_1()
    f10_2()
    f10_3()
    f11_2()
    f12_2()

