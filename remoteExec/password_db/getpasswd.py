#!/usr/bin/python
# coding: utf-8


import sys
import pwdctrl as pctl


if __name__ == "__main__":
    try:
        ip = sys.argv[1]
    except IndexError as e:
        print("Usage:", sys.argv[0], "${IP}")
        sys.exit()
    pwd = pctl.PWDCTRL("testdb")
    password = pwd.get_pwd(ip)

    print(password)
