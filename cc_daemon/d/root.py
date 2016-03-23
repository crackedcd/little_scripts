# coding: utf-8


import os
import d.daemon
import d.call


class DaemonRoot(d.daemon.Daemon):
    '''
    daemon usage test example.
    '''

    def __init__(self, module_name):
        str_cwd = os.getcwd() + "/log/"

        if not os.path.exists(str_cwd):
            os.mkdir(str_cwd)

        pid_file = "%s/%s_pid.pid" % (str_cwd, module_name)
        stdout_file = "%s/%s_stdout.log" % (str_cwd, module_name)
        stderr_file = "%s/%s_stderr.log" % (str_cwd, module_name)

        self.init_daemon(pid_file, stdout_file, stderr_file)


    def run_daemon(self):
        '''
        override daemon.Daemon.run_daemon() function.
        '''

        self.__start_service()


    def __start_service(self):
        '''
        main function.
        run service here.
        '''

        # do something here.

        c = d.call.CallLoop()
        c.loop()

        print("service is running...")


