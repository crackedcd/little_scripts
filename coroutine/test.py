#!/usr/bin/env python

from gevent import monkey; monkey.patch_all()
import gevent
from multiprocessing.dummy import Pool as ThreadPool
import threading
import time


def pp(string):
    string1, string2 = string
    print("%s->%s" % (string1, string2))
    time.sleep(0.5)

def normal_p(i_list):
    for i in i_list:
        pp(i)

def map_p(i_list):
    pool = ThreadPool(20)
    pool.map(pp, i_list)
    pool.close()
    pool.join()


def async_p(i_list):
    p = ThreadPool(20)
    for l in i_list:
        p.apply_async(pp, args=(l,))
    p.close()
    p.join()


def thread_p(i_list):
    lock = threading.Lock()
    for l in i_list:
        lock.acquire()
        t = threading.Thread(target = pp, args = (l, ))
        lock.release()
        t.start()
    t.join()


def gevent_p(i_list):
    spawn_list = []
    for l in i_list:
        spawn_list.append(gevent.spawn(pp, l))
    gevent.joinall(spawn_list)


def stackless_p(i_list):
    for l in i_list:
        stackless.tasklet(ppp)(l)
    stackless.run()


if __name__ == "__main__":
    i_list = []
    for i in range(1, 10):
        i_list.append(("number", i))

    #print(i_list)
    begin = time.time()
    normal_p(i_list)
    #map_p(i_list)
    #async_p(i_list)
    #thread_p(i_list)
    #gevent_p(i_list)
    end = time.time()
    print("elapsed: %ss." % (end - begin))

