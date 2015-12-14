#!/usr/bin/python
# coding: utf-8


import sqlite3
import os
import sys


class DB:

    def __init__(self, database):
        __this_script = os.path.realpath(sys.argv[0])
        __real_path = os.path.split(__this_script)[0]
        __database = "".join([__real_path, "/database/", database])
        self.__conn = sqlite3.connect(__database)

    def query(self, query, data = ()):
        # 接受两个参数, 第一个是SQL语句模板, 第二个是值的集合
        #print(query)
        cursor = self.__conn.execute(query, data)
        result = []
        for rows in cursor:
            result.append(rows)
        return result


if __name__ == "__main__":
    pass


