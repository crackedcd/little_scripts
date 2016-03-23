# coding: utf-8


import sys
import d.root


class Main(object):

    def __init__(self):
        self.__root = d.root.DaemonRoot("daemon")

    def run_daemon(self, method):
        if method == "start":
            self.__root.start_daemon()
        elif method == "stop":
            self.__root.stop_daemon()
        elif method == "restart":
            self.__root.restart_daemon()


if __name__ == '__main__':

    main = Main()

    if len(sys.argv) == 2:
        call_methods = ["start", "stop", "restart"]
        main.run_daemon(sys.argv[1])
    else:
        print(''' Usage: python run.py [start|stop|restart] ''')

