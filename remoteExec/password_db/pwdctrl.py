#!/usr/bin/python
# coding: utf-8


import database


class DBUSE(database.DB):

    def set(self, query, data):
        return self.query(query, data)

    def get(self, query):
        return self.query(query)


class PWDCTRL(DBUSE):

    def get_pwd(self, ip):
        sql = "".join(["select pwd from resource where ip = '", ip, "'"])
        return self.get(sql)[0][0]


if __name__ == "__main__":
    pass

