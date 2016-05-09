# coding: utf-8


import os
import sys
import logging
from logging.handlers import RotatingFileHandler


class Log(object):
    '''
    only log() methods can be called.

    Usage example:
        import log
        l = log.Log("my_module_name")
        l.log()
        # call my own methods.
    '''

    def __init__(self, module_name):

        # os.getcwd() returns current working directory of a process.
        # str_cwd = os.getcwd() + "/log/" + module_name + "/"
        # sys.path[0] returns current executing python script directory.
        str_cwd = sys.path[0] + "/log/" + module_name + "/"

        if not os.path.exists(str_cwd):
            os.mkdir(str_cwd)

        self.__stdout_file = "%s/stdout.log" % str_cwd
        self.__stderr_file = "%s/stderr.log" % str_cwd

        self.__max_size = 1  # unit MB.
        self.__max_count = 5


    def __stdout(self, msg):
        logging.basicConfig(level=logging.DEBUG,
                            format='%(asctime)s %(filename)s [line:%(lineno)d] %(levelname)s %(message)s',
                            datefmt='%b-%Y-%d %H:%M:%S',
                            filename=self.__stdout_file,
                            filemode='w')
        logging.info(msg)

    def __stderr(self, msg):
        logging.basicConfig(level=logging.DEBUG,
                            format='%(asctime)s %(filename)s [line:%(lineno)d] %(levelname)s %(message)s',
                            datefmt='%b-%Y-%d %H:%M:%S',
                            filename=self.__stderr_file,
                            filemode='w')
        logging.error(msg)

    def __rotate(self):
        stdout_handler = RotatingFileHandler(self.__stdout_file, maxBytes=100*1024*1024, backupCount=10)
        stdout_handler.setLevel(logging.INFO)
        stderr_handler = RotatingFileHandler(self.__stderr_file, maxBytes=100*1024*1024, backupCount=10)
        stderr_handler.setLevel(logging.ERROR)

        formatter = logging.Formatter('%(name)s: %(levelname)s %(message)s')
        stdout_handler.setFormatter(formatter)
        stderr_handler.setFormatter(formatter)

        logging.getLogger('').addHandler(stdout_handler)
        logging.getLogger('').addHandler(stderr_handler)

    def __log_rotate(self, file):
        with open(file) as f:
            if len(f.read()) > self.__max_size * 1024 * 1024:
                for i in reversed(range(1, self.__max_count)):
                    old_file = file + '.' + str(i + 1)
                    new_file = file + '.' + str(i)
                    if os.path.exists(new_file):
                        os.rename(new_file, old_file)
                os.rename(file, new_file)

    def log(self):
        '''
        duplicate sys.stdout/sys.stderr file description to logfile.
        '''
        # create std files.
        sys.stdout.flush()
        sys.stderr.flush()
        fd_stdout = open(self.__stdout_file, "a+")
        fd_stderr = open(self.__stderr_file, "a+")

        # bind std pipes.
        # os.dup2(fd_stdout.fileno(), sys.stdout.fileno())
        # os.dup2(fd_stderr.fileno(), sys.stderr.fileno())
        default_stdout = sys.stdout
        default_stderr = sys.stderr
        sys.stdout = fd_stdout
        sys.stderr = fd_stderr

        self.__log_rotate(self.__stdout_file)
        self.__log_rotate(self.__stderr_file)

