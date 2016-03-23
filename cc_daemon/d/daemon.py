# coding: utf-8                                                                                                           


import os
import sys
import atexit
import time


class Daemon(object):
    '''
    main daemon.
    Usage: extend Deamon class and override run() method function.
    '''

    def __init__(self):
        self.__str_error_msg = ""
        self.__stdout_file = ""
        self.__stderr_file = ""
        self.__pid_file = ""

    def init_daemon(self, pid_file, stdout_file="/dev/null", stderr_file="/dev/null"):
        '''
        init daemon.
        '''

        self.__stdout_file = stdout_file
        self.__stderr_file = stderr_file
        self.__pid_file = pid_file

    def __del_pid(self):
        '''
        delete pid file.
        '''
        try:
            os.remove(self.__pid_file)
            return True
        except Exception as ex:
            self.__str_error_msg = "create daemon pid file %s failed: %d(%s)\n" % (self.__pid_file, ex.errno, ex.strerror)


    def __create_daemon(self):
        '''
        create daemon.
        '''

        try:
            # fork sub process.
            try:
                sub_proc_pid = os.fork()
                # if return pid true, prcess created successfully.
                if sub_proc_pid > 0:
                    # exit father process.
                    sys.exit(0)
            except OSError as ex:
                self.__str_error_msg = "create daemon fork #1 failed: %d(%s)\n" % (ex.errno, ex.strerror)
                return False
            # change work dir to local root dir.
            os.chdir("/")
            # set this process as processor group leader.
            os.setsid()
            # set umask as 0, grant all privilges.
            os.umask(0)

            # for sub process by last forked process.
            try:
                i_sub_proc_pid = os.fork()
                if i_sub_proc_pid > 0:
                    # exit last forked process as it is father.                          
                    sys.exit(0)
            except OSError as ex:
                self.__str_error_msg = "create daemon fork #2 failed: %d(%s)\n" % (ex.errno, ex.strerror)
                return False

            # create std files.                                                          
            sys.stdout.flush()
            sys.stderr.flush()
            fd_stdout = open(self.__stdout_file, "a+")
            fd_stderr = open(self.__stderr_file, "a+")

            # create std pipes.                                                          
            os.dup2(fd_stdout.fileno(), sys.stdout.fileno())
            os.dup2(fd_stderr.fileno(), sys.stderr.fileno())

            # delete pid file.                                                           
            ret = atexit.register(self.__del_pid)
            if ret is False:
                return False

            # write pid file.                                                            
            proc_pid = str(os.getpid())
            open(self.__pid_file, "w+").write("%s\n" % proc_pid)
            if os.path.exists(self.__pid_file) is False:
                self.__str_error_msg = "create daemon write pid file failed: (%s)\n" % ex
                return False

        except Exception as ex:
            self.__str_error_msg = "create daemon failed: %s\n" % ex
            return False

    def start_daemon(self):
        '''
        start daemon.
        '''

        try:
            pid_file = open(self.__pid_file, "r")
            pid = int(pid_file.read().strip())
            pid_file.close()
        except Exception as ex:
            pid = None

        # check if pid is exists.                                                        
        if pid:
            self.__str_error_msg = "pid file %s already exists. daemon already running.\n" % self.__pid_file
            sys.stderr.write(self.__str_error_msg)
            sys.exit(-1)

        # start daemon.                                                                  
        ret = self.__create_daemon()
        if ret is False:
            sys.stderr.write(self.__str_error_msg)
            sys.exit(-1)

        self.run_daemon()


    def stop_daemon(self):
        '''
        stop daemon.
        '''

        try:
            pid_file = open(self.__pid_file, "r")
            pid = int(pid_file.read().strip())
            pid_file.close()
        except Exception as ex:
            pid = None

        # check if pid is exists.
        if not pid:
            self.__str_error_msg = "pid file %s does not exists. daemon not running.\n" % self.__pid_file
            sys.stderr.write(self.__str_error_msg)
            sys.exit(-1)

        # kill alive processes.
        try:
            str_cmd = ''' ps aux | fgrep -v %d | awk '{if($3=="%d") print $2} END{print "%d"}' | xargs kill -9 ''' \
                % (pid, pid, pid)
            os.system(str_cmd)
            # os.kill(pid, SIGTERM)
            time.sleep(0.1)

            # clear pid file.
            if os.path.exists(self.__pid_file):
                os.remove(self.__pid_file)

        except Exception as ex:
            str_ex = str(ex)
            if str_ex.find("No such process") != -1:
                if os.path.exists(self.__pid_file):
                    os.remove(self.__pid_file)
            else:
                print(str_ex)
                sys.exit(-1)

    def restart_daemon(self):
        '''
        restart daemon.
        '''

        try:
            self.stop_daemon()
            self.start_daemon()
        except Exception as ex:
            self.__str_error_msg = "daemon restart error: %s\n" % ex
            sys.stderr.write(self.__str_error_msg)
            sys.exit(-1)

    def run_daemon(self):
        '''
        should be override by sub class.
        '''
        pass

