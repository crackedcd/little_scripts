# coding: utf-8


import sys
import time
import d.modules.ping


class CallLoop(object):


    def __init__(self):
        '''
        statement specific objects here as self private variables and functions.
        '''
        self.__ping = d.modules.ping.Ping()


    def loop(self):
        '''
        outter methods call this class by loop() method.
        '''

        # time step length (s).
        time_step_seconds = 2

        while True:
            sys.stdout.write("%s\n" % time.ctime())
            sys.stdout.flush()
            time.sleep(time_step_seconds)

            # call really methods.
            self.__run()


    def __run(self):
        '''
        really methods defined in self.__init__() and running here in this function.
        '''

        self.__ping.run()

