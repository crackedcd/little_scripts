# decorator

## 1.基本的嵌套高阶函数

```python
def wholelogin(func):
    def __innerlogin():
        print('enter login.')
        func()
        print('exit login.')
    return __innerlogin

def login():
    print('is login.')

wholelogin(login)
```

*执行结果:*

```
enter login.
is login.
exit login.
```

## 2.函数本身是对象, 将高阶函数赋值给变量

```python
def wholelogin(func):
    def __innerlogin():
        print('enter login.')
        func()
        print('exit login.')
    return __innerlogin

def login():
    print('is login.')

a = wholelogin(login)
a()
```

*执行结果:*

```
enter login.
is login.
exit login.
```

## 3.赋值的时候把高阶函数赋值给一个和内嵌函数同名的变量

```python
def wholelogin(func):
    def __innerlogin():
        print('enter login.')
        func()
        print('exit login.')
    return __innerlogin

def login():
    print('is login.')

login = wholelogin(login)
login()
```

*执行结果:*

```
enter login.
is login.
exit login.
```

## 4.改成decorator

```python
def wholelogin(func):
    def __innerlogin():
        print('enter login.')
        func()
        print('exit login.')
    return __innerlogin

@wholelogin
# 这个@func_parent的出现, 说明它下方的第一个函数func_son会被解释成一个decorator, 且转换到func_son同名的变量.
# 即login = wholelogin(login)
# 中间可以任意加空行或者注释, 但是不可以有其他逻辑或者变量赋值
def login():
    print('is login.')

login()
```

*执行结果:*

```
enter login.
is login.
exit login.
```

## 5.有参数的decorator

### 1) 函数带参数

```python
def wholelogin(func):
    def __innerlogin(login_args):
        print('enter login.')
        func(login_args)
        print('exit login.')
    return __innerlogin

@wholelogin
def login(name):
    print('%s is login.' % name)

login('cc')
```

*执行结果:*

```
enter login.
cc is login.
exit login.
```

### 2) 装饰器带参数 (再增加一层函数阶级)

```python
def outter_wholelogin(decorator_args):
    def wholelogin(func):
        def __innerlogin(login_args):
            print('get param: %s.' % decorator_args)
            print('enter login.')
            func(login_args)
            print('exit login.')
        return __innerlogin
    return wholelogin

@outter_wholelogin(decorator_args='XXX')
def login(name):
    print('%s is login.' % name)

login('cc')
```

*执行结果:*

```
get param: this is XXX.
enter login.
is login.
exit login.
```

> 整个login('cc')的调用过程是:
>
> [**decorated**]login('cc') => 
>
> outter_wholelogin('XXX') => 
>
> wholelogin[**with closure value 'XXX'**](login)('cc') => 
>
> __decorator('cc')[**use value 'XXX'**] => 
>
> [**real**]login('cc')

## 6.有返回的decorator, 低阶函数返回, 高阶函数将低阶函数的返回返回

```python
def wholelogin(func):
    def __innerlogin(login_args):
        result = func(login_args)
        return result
    return __innerlogin

@wholelogin
def login(name):
    if name == 'cc':
        return True
    else:
        return False

result1 = login('c')
result2 = login('cc')
result3 = login('ccc')
print(result1)
print(result2)
print(result3)
```

*执行结果:*

```
False
True
False
```

## 7.多个装饰器的顺序

```python
def wholelogin(func):
    def __innerlogin(login_args):
        print('enter login.')
        func(login_args)
        print('exit login.')
    return __innerlogin

def other(func):    # define an other decorator
    def __decorator(login_args):
        print('***other decorator begin***')
        func(login_args)
        print('***other decorator end***')
    return __decorator


print('decorator WHOLELOGIN:')
@wholelogin
def login(name):
    print('%s is login.' % name)

login('cc')
 
print('decorator : 1) OTHERS 2) WHOLELOGIN')
@other
@wholelogin
def login(name):
    print('%s in login.' % name)

login('cc')

 
print('decorator: 1) WHOLELOGIN 2) OTHERS')
@wholelogin
@other
def login(name):
    print('%s in login.' % name)
 
login('cc')
```

*执行结果:*

```python
decorator WHOLELOGIN:
enter login.
cc is login.
exit login.
decorator : 1) OTHERS 2) WHOLELOGIN
***other decorator begin***
enter login.
cc in login.
exit login.
***other decorator end***
decorator: 1) WHOLELOGIN 2) OTHERS
enter login.
***other decorator begin***
cc in login.
***other decorator end***
exit login.
```

> 写在前面的decorator在"外层", 先调用.
