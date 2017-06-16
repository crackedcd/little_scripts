#!/usr/bin/env python
# coding: utf-8


from gevent import monkey; monkey.patch_socket()
import gevent
import redis
import time
from functools import wraps


class HELP(object):

    def __init__(self):
        help_str = '''
[root@cc django]# cat redis_servers
127.0.0.1 6379
1 a
2   b
3   c
4   d
  
  4   f
  6   4
'''
        print(help_str)


class RDS(object):

    def __init__(self, server_list_file):
        #self.__rds_list = []
        self.__rds_dict = {}
        with open(server_list_file) as fd:
            for server in fd.readlines():
                if server and server.strip() != "":
                    ip, port = server.split()[0], server.split()[1]
                    self.__rds_dict[ip] = port
                    #self.__rds_list.append(self.__rds_dict)

    def __timethis(func):
        def __wrapper(*args, **kwargs):
            start = time.perf_counter()
            r = func(*args, **kwargs)
            end = time.perf_counter()
            print("Time cost: %5f s." % (end - start))
            return r
        return __wrapper

    @staticmethod
    @__timethis
    def __info(ip, p):
        try:
            r = redis.Redis(host = ip, port = p, db = 0, socket_timeout = 2)
            info = r.info()
            print("%s:%s -> %s" % (ip, p, info["used_memory_peak_human"]))
        except (redis.exceptions.ConnectionError, ValueError) as e:
            print("ERROR: %s:%s connection failed." % (ip, p))

    def reversal(self):
        spawn_list = []
        for ip, port in self.__rds_dict.items():
            spawn_list.append(gevent.spawn(RDS.__info, ip, port))
        #for s in self.__rds_list:
            #for ip, port in s.items():
                #spawn_list.append(gevent.spawn(self.__info, ip, port))
        gevent.joinall(spawn_list)


if __name__ == "__main__":
    #h = HELP()
    rds = RDS("./redis_servers")
    rds.reversal()

