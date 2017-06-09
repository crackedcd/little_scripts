#!/usr/bin/env python
# coding: utf-8


import time
from functools import wraps
from contextlib import contextmanager

## timethis装饰器
def timethis(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        start = time.perf_counter()
        r = func(*args, **kwargs)
        end = time.perf_counter()
        print('{}.{} : {}'.format(func.__module__, func.__name__, end - start))
        return r
    return wrapper

## timeblock上下文管理器
@contextmanager
def timemgr(label):
    start = time.perf_counter()
    try:
        yield
    finally:
        end = time.perf_counter()
        print('{} : {}'.format(label, end - start))

## 需要计算耗时的函数
def loop_count(n):
    while n > 0:
        n -= 1


## 装饰器实例
@timethis
def countdown_timethis(n):
    loop_count(n)

# 上下文管理器实例
def countdown_contextmgr(n):
    with timemgr("count time"):
        loop_count(n)

# go
if __name__ == "__main__":
    countdown_timethis(10000)
    countdown_contextmgr(10000)

