# coding: utf-8


import sys
import time
import threading
import d.modules.ping
import d.modules.alert
import d.modules.alert2


class CallLoop(object):


    def __init__(self):
        '''
        statement specific objects here as self private variables and functions.
        '''
        self.__ping = d.modules.ping.Ping()
        self.__alert = d.modules.alert.Alert()
        self.__alert2 = d.modules.alert2.Alert2()


    def send_alarm(self):
        '''
        outter methods call this class to send alarm immediately by send_alarm() method.
        '''

        # time step length (s).
        time_step_seconds = 10

        while True:
            sys.stdout.write("%s\n" % time.ctime())
            sys.stdout.flush()
            time.sleep(time_step_seconds)

            # call really methods.
            self.__alarm()


    def send_info(self):
        '''
        outter methods call this class to send info regularly by send_info() method.
        '''

        # time step length (s).
        time_step_seconds = 1

        while True:
            sys.stdout.write("%s\n" % time.ctime())
            sys.stdout.flush()
            time.sleep(time_step_seconds)

            # call really methods.
            self.__info()


    def __alarm(self):
        '''
        really methods defined in self.__init__() and running here in this function.
        '''

        # append threading task.
        t = threading.Thread(target = self.__ping.run())
        t.start()

        # execute all threading task.
        t.join()


    def __info(self):
        '''
        really methods defined in self.__init__() and running here in this function.
        '''

        # append threading task.
        t = threading.Thread(target = self.__alert.run())
        t.start()
        t = threading.Thread(target = self.__alert2.run())
        t.start()

        # execute all threading task.
        t.join()

