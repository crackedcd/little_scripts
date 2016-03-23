# coding: utf-8


import os
import logging
from logging.handlers import import RotatingFileHandler


class Log(object):

    def __init__(self, module_name):

        str_cwd = os.getcwd + "/log/" + module_name + "/"

        if not os.path.exists(str_cwd):
            os.mkdir(str_cwd)

        self.__stdout_file = "%s/stdout.log" % str_cwd
        self.__stderr_file = "%s/stderr.log" % str_cwd


    def stdout(self, msg):
        logging.basicConfig(level=logging.DEBUG,
                            format='%(asctime)s %(filename)s [line:%(lineno)d] %(levelname)s %(message)s',
                            datefmt='%b-%Y-%d %H:%M:%S',
                            filename=self.__stdout_file,
                            filemode='w')
        logging.info(msg)

    def stderr(self, msg):
        logging.basicConfig(level=logging.DEBUG,
                            format='%(asctime)s %(filename)s [line:%(lineno)d] %(levelname)s %(message)s',
                            datefmt='%b-%Y-%d %H:%M:%S',
                            filename=self.__stderr_file,
                            filemode='w')
        logging.error(msg)

    def rotate(self):
        stdout_handler = RotatingFileHandler(self.__stdout_file, maxBytes=100*1024*1024, backupCount=10)
        stdout_handler.setLevel(logging.INFO)
        stderr_handler = RotatingFileHandler(self.__stderr_file, maxBytes=100*1024*1024, backupCount=10)
        stderr_handler.setLevel(logging.ERROR)

        formatter = logging.Formatter('%(name)s: %(levelname)s %(message)s')
        stdout_handler.setFormatter(formatter)
        stderr_handler.setFormatter(formatter)

        logging.getLogger('').addHandler(stdout_handler))
        logging.getLogger('').addHandler(stderr_handler))

