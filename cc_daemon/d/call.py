# coding: utf-8


import sys
import time
import threading
import d.modules.ping
import d.modules.alert
import d.modules.alert2
import d.modules.cmq_monitor


class CallLoop(object):


    def __init__(self):
        '''
        statement specific objects here as self private variables and functions.
        '''
        # time step length (s).
        self.__info_step_seconds = 60
        self.__alarm_step_seconds = 2


    def send_alarm(self):
        '''
        outter methods call this class to send alarm immediately by send_alarm() method.
        '''


        # while True:
            # call really methods.
            # threading.Thread(target = self.__alarm()).start()

            # sys.stdout.write("%s\n" % time.ctime())
            # sys.stdout.flush()
            # time.sleep(self.__alarm_step_seconds)

        threading.Timer(self.__alarm_step_seconds, self.__alarm).start()

    def send_info(self):
        '''
        outter methods call this class to send info regularly by send_info() method.
        '''

        # while True:
            # call really methods.
            # threading.Thread(target = self.__info()).start()

            # sys.stdout.write("%s\n" % time.ctime())
            # sys.stdout.flush()
            # time.sleep(time_step_seconds)

        threading.Timer(self.__info_step_seconds, self.__info).start()


    def __alarm(self):
        '''
        really methods defined in self.__init__() and running here in this function.
        '''

        '''
        # append threading task.
        t = threading.Thread(target = self.__ping.run)
        t.start()

        # execute all threading task.
        t.join()
        '''

        #ping = d.modules.ping.Ping()
        #threading.Thread(target = ping.run).start()

        threading.Timer(self.__alarm_step_seconds, self.__alarm).start()


    def __info(self):
        '''
        really methods defined in self.__init__() and running here in this function.
        '''

        '''
        # append threading task.
        t = threading.Thread(target = self.__alert.run)
        t.start()
        t = threading.Thread(target = self.__alert2.run)
        t.start()

        # execute all threading task.
        t.join()
        '''

        #alert = d.modules.alert.Alert()
        #threading.Thread(target = alert.run).start()
        #alert2 = d.modules.alert2.Alert2()
        #threading.Thread(target = alert2.run).start()

        cmq_monitor = d.modules.cmq_monitor.CMQMonitor()
        threading.Thread(target = cmq_monitor.run).start()

        threading.Timer(self.__info_step_seconds, self.__info).start()

