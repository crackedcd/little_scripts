import time
import asyncio
import functools


now = lambda: time.time()
LINE = "%s" % ("*" * 50)


# async def 定义协程对象, 该对象不可直接执行, 必须加入事件循环调用
async def go(s):
    print("asyncio waiting: %s" % s)


def one_coroutine():
    start = now()

    # 这个coroutine是不能直接执行的, 直接执行coroutine(), 会提示coroutine 'go' was never awaited
    coroutine = go("go_async_coroutine")
    # 创建asyncio事件循环
    loop = asyncio.get_event_loop()
    # 使用run_until_complete将协程对象注册到事件循环, 也即是把协程对象包装成了任务(task)对象, 并启动
    # 也可以 task = asyncio.ensure_future(coroutine) 创建task对象
    task = loop.create_task(coroutine)
    # 在执行之前, print(task)可以看到task现在是pending状态, pending means "about to happen or waiting to happen"
    print(task)
    loop.run_until_complete(task)
    # 在执行之后, print(task)可以看到task现在是finished状态
    print(task)
    # 因为上面这里只有一个task, 所以也可以不创建task, 直接loop.run_until_complete(coroutine)

    end = now()
    print("time cost: %s" % (end - start))


#############################################################################################


async def go_callback(s):
    print("asyncio callback waiting: %s" % s)
    return "done after %s" % s


def callback(p, future):
    print("callback is called: %s" % future.result())
    print("callback param is: %s" % p)


def callback_coroutine():
    start = now()

    # coroutine执行结束时候会调用回调函数, 并通过参数future获取协程执行的结果. 创建的task和回调里的future对象, 实际上是同一个对象
    coroutine = go_callback("go_callback_coroutine")
    loop = asyncio.get_event_loop()
    task = asyncio.ensure_future(coroutine)
    # functools.partial创建偏函数
    task.add_done_callback(functools.partial(callback, "callback string"))
    loop.run_until_complete(task)
    print("task return: %s" % task.result())

    end = now()
    print("time cost: %s" % (end - start))


#############################################################################################


async def go_wait(s):
    print("asyncio sleep waiting: %s" % s)
    await asyncio.sleep(2)
    return "done after %s" % s


def wait_coroutine():
    start = now()

    coroutine = go_wait("go_wait_coroutine")
    loop = asyncio.get_event_loop()
    task = asyncio.ensure_future(coroutine)
    loop.run_until_complete(task)
    print("task return: %s" % task.result())

    end = now()
    print("time cost: %s" % (end - start))


#############################################################################################


async def go_multi(s):
    print("asyncio multi waiting: %s" % s)
    await asyncio.sleep(s)
    return "done after %s seconds." % s


def multi_coroutine():
    start = now()

    coroutine1 = go_multi(1)
    coroutine2 = go_multi(2)
    coroutine3 = go_multi(4)

    # 创建多个协程的列表, 然后将这些协程注册到事件循环中
    tasks = [
        asyncio.ensure_future(coroutine1),
        asyncio.ensure_future(coroutine2),
        asyncio.ensure_future(coroutine3)
    ]
    loop = asyncio.get_event_loop()
    loop.run_until_complete(asyncio.wait(tasks))

    for task in tasks:
        print("task return: %s" % task.result())

    end = now()
    print("time cost: %s" % (end - start))


#############################################################################################


async def go_nesting(s):
    print("asyncio nesting waiting: %s" % s)
    await asyncio.sleep(s)
    return "done after %s seconds." % s


async def nesting_main():
    coroutine1 = go_nesting(1)
    coroutine2 = go_nesting(2)
    coroutine3 = go_nesting(4)

    tasks = [
        asyncio.ensure_future(coroutine1),
        asyncio.ensure_future(coroutine2),
        asyncio.ensure_future(coroutine3)
    ]
    dones, pendings = await asyncio.wait(tasks)

    for task in dones:
        print("task return: %s" % task.result())

def nesting_coroutine():
    start = now()

    loop = asyncio.get_event_loop()
    loop.run_until_complete(nesting_main())

    end = now()
    print("time cost: %s" % (end - start))


#############################################################################################
# 总的来说, 使用async可以定义协程对象, 使用await可以针对耗时的操作进行挂起
# 但是我还是选择继续用gevent
#############################################################################################


if __name__ == "__main__":
    one_coroutine()
    print(LINE)
    callback_coroutine()
    print(LINE)
    wait_coroutine()
    print(LINE)
    multi_coroutine()
    print(LINE)
    nesting_coroutine()
    print(LINE)


