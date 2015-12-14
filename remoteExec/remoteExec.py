#!/usr/bin/env python
# coding: utf-8

'''
    Author: yuchao

    Last modified: 2015-09-24 14:43

    Filename: remoteExec.py

    Description: exec bash shell commands on remote servers.
                 depends on python package: 'Crypto', 'ecdsa'.
'''


from gevent import monkey; monkey.patch_all()
import gevent
import paramiko  # depends on pkg: 'Crypto', 'ecdsa'
from pprint import pprint
from multiprocessing import Pool
import threading
import subprocess
import time
import os
import stackless
import sys


def remote_cmd(ip, pwd, cmd):
    '''
    ssh and run command on remote server.
    '''

    usr = 'root'  # tx default ssh user.
    port = 36000  # tx default ssh port.

    try:
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        # client.load_system_host_keys()
        ssh.connect(ip, port, usr, pwd)
        # (stdin, stdout, stderr) = ssh.exec_command(cmd)
        result_list = ssh.exec_command(cmd)
        format_paramiko_out(result_list)
    except paramiko.ssh_exception.BadAuthenticationType as bad_auth_e:
        print("%s. %s can't be login by %s." % (bad_auth_e, ip, pwd))


def remote_cmd_schedule(ip, pwd, cmd):
    '''
    almost like remote_cmd(), but use stackless.schedule().
    '''
    
    usr = 'root'  # tx default ssh user.
    port = 36000  # tx default ssh port.

    try:
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        # client.load_system_host_keys()
        ssh.connect(ip, port, usr, pwd)
        result_list = ssh.exec_command(cmd)
        stackless.schedule()  # when ssh.exec_command BLOCK(spend a lot of time), schedule this function to the rear of task queue, call next function.
        format_paramiko_out(result_list)
    except paramiko.ssh_exception.BadAuthenticationType as bad_auth_e:
        print("%s. %s can't be login by %s." % (bad_auth_e, ip, pwd))


def send_file(ip, pwd, local_path = os.path.split(os.path.realpath(sys.argv[0]))[0], remote_path = '/data/', file = sys.argv[1]):
    '''
    sftp send file with remote server.
    '''
    usr = 'root'  # tx default ssh user.
    port = 36000  # tx default ssh port.
    t = paramiko.Transport((ip, port))  
    try:
        t.connect(username = usr, password = pwd)
        sftp = paramiko.SFTPClient.from_transport(t)
        sftp.put(os.path.join(local_path, file), os.path.join(remote_path, file))
    except paramiko.ssh_exception.BadAuthenticationType as bad_auth_e:
        print("%s. %s can't be login by %s." % (bad_auth_e, ip, pwd))
    except paramiko.ssh_exception.SSHException as ssh_e:
        print("%s. %s can't be login by %s." % (ssh_e, ip, pwd))
    finally:
        t.close()


def getpasswd(ip):
    '''
    get password by given IP.
    '''

    try:
        passwd_fd = os.popen("/root/bin/getpasswd " + ip)
        pwds_list = []
        for pwds in passwd_fd:
            pwd = pwds.split("\n")[0]
            pwds_list.append(pwd)
    except TypeError as te:
        print("%s. IP [%s] can't get password in database." % (te, ip))
    except BrokenPipeError as be:
        print("%s. IP [%s] can't get password in database." % (be, ip))
        return

    return pwds_list[0]


def format_paramiko_out(paramiko_out_list):
    '''
    format paramiko out LIST to STRING.
    paramiko out is a list, [0] for stdin, [1] for stdout, [2] for stderr
    this function print result to shell stdout directly.
    '''

    out_list = paramiko_out_list[1].readlines() + paramiko_out_list[2].readlines()
    for ln in list(out_list):
        print('%s' % ln.strip())
    minus_str = '-' * len(ln)  # string like many '------'
    print('%s' % minus_str)


def multi_exec(ip_pwd_dict, cmd):
    '''
    multi processing to run remote_cmd().
    count(processings) == count(CPUs)
    '''

    print_ip_cmd = "echo; /sbin/ifconfig eth1 | awk -F'[ :]+' 'NR==2{print $4}'; echo; "
    processor_count = 16  # almost like CPUs number.
    p = Pool(processor_count)
    count = 0
    for (ip, pwd) in list(ip_pwd_dict.items()):
        p.apply_async(remote_cmd, (ip, pwd, print_ip_cmd + cmd))
        count += 1
    print('%d servers done.\n%s' % (count, '*' * 100))
    p.close()
    p.join()


def stackless_exec(ip_pwd_dict, cmd):
    '''
    stackless to run remote_cmd().
    '''

    print_ip_cmd = "echo; /sbin/ifconfig eth1 | awk -F'[ :]+' 'NR==2{print $4}'; echo; "

    for (ip, pwd) in list(ip_pwd_dict.items()):
        stackless.tasklet(remote_cmd_schedule)(ip, pwd, print_ip_cmd + cmd)

    stackless.run()

    print('\n%d servers done.\n' % len(list(ip_pwd_dict.items())))
    # print("Task finished, press 'Ctrl + C' to interrupt paramiko.")


def coroutine_exec(ip_pwd_dict, cmd):
    '''
    gevent coroutine to run remote_cmd().
    '''

    print_ip_cmd = "echo; /sbin/ifconfig eth1 | awk -F'[ :]+' 'NR==2{print $4}'; echo; "

    spawn_list = []
    for (ip, pwd) in list(ip_pwd_dict.items()):
        spawn_list.append(gevent.spawn(remote_cmd, ip, pwd, cmd))
    gevent.joinall(spawn_list)


def threading_exec(ip_pwd_dict, cmd):
    '''
    multi threading to run remote_cmd().
    count(threadings) == count(JOBs)
    NOTICE: may occur many display error, use multi_exec() instead of this.

    TODO(): this function would call FUTEX_WAIT_BITSET_PRIVATE, DO NOT use it!

    '''

    lock = threading.Lock()
    print_ip_cmd = "echo; /sbin/ifconfig eth1 | awk -F'[ :]+' 'NR==2{print $4}'; echo; "

    threads_list = []
    for (ip, pwd) in list(ip_pwd_dict.items()):
        lock.acquire()
        t = threading.Thread(target = remote_cmd, args = (ip, pwd, print_ip_cmd + cmd))
        lock.release()
        t.start()
        threads_list.append(t)
    for th in list(threads_list):
        th.join()


def serial_exec(ip_pwd_dict, cmd):
    '''
    serial exec to run remote_cmd().
    this function is slower but display better than multi_exec().
    '''

    for (ip, pwd) in list(ip_pwd_dict.items()):
        print('running on [%s] :' % ip)
        remote_cmd(ip, pwd, cmd)


def gen_remote_dict(ip_list):
    '''
    generate an {ip: pwd} dict by ip list.
    '''

    remote_dict = {}
    for ip in list(ip_list):
        remote_dict[ip] = getpasswd(ip)

    return remote_dict


def get_iplists(file_name):
    '''
    get IP lists from iplists file.
    '''
    ip_list = []
    with open(file_name) as fd:
        for lines in fd.readlines():
            ln = lines.strip()
            if ((ln) and (ln != '')):
                ip_list.append(ln)
    return ip_list


def get_cmds(file_name):
    '''
    get CMDs lists from cmds file.
    '''
    cmds_list = []
    with open(file_name) as fd:
        for lines in fd.readlines():
            cmds_list.append(lines.strip())
    return cmds_list


def exec_cmds(ips_list, cmds_list, func = 'multi'):
    '''
    exec cmds_list on remote ips_list by:
        1) multi_exec (default)
        2) serial_exec
        3) threading_exec
    '''
    remote_dict = gen_remote_dict(ips_list)
    if func == 'multi':
        for cmd in list(cmds_list):
            multi_exec(remote_dict, cmd)
    elif func == 'serial':
        for cmd in list(cmds_list):
            serial_exec(remote_dict, cmd)
    elif func == 'threading':
        for cmd in list(cmds_list):
            threading_exec(remote_dict, cmd)
    elif func == 'coroutine':
        for cmd in list(cmds_list):
            coroutine_exec(remote_dict, cmd)
    elif func == 'stackless':
        for cmd in list(cmds_list):
            stackless_exec(remote_dict, cmd)



def exec_files(ips_list, scripts_file, func = 'multi', script_type = 'bash'):
    '''
    1) send scripts_file to remote servers.
    2) execute scripts_file on remote server.

    run exec_file on remote ips_list by:
        1) multi_exec (default)
        2) serial_exec
        3) threading_exec

    scripts_file can be 2 types, 'bash' or 'python'.
    '''

    remote_dict = gen_remote_dict(ips_list)

    if script_type == 'bash':
        cmd = "/bin/bash /data/" + sys.argv[1]
        for (ip, pwd) in list(remote_dict.items()):
            send_file(ip, pwd)

    if func == 'multi':
        multi_exec(remote_dict, cmd)
    elif func == 'serial':
        serial_exec(remote_dict, cmd)
    elif func == 'threading':
        threading_exec(remote_dict, cmd)
    elif func == 'coroutine':
        coroutine_exec(remote_dict, cmd)
    elif func == 'stackless':
        stackless_exec(remote_dict, cmd)


if __name__ == '__main__':
    '''
    there are 2 methods to use this script:
        1) execute CMDs on remote servers:
            define cmds_file
            use get_iplists() to generate cmds_list.
            use exec_cmds() to run cmds on remote server.
        2) execute SCRIPTs on remote servers:
            define scripts_file
            use exec_files(), this function call send_file() to send scripts_file to remote servers, then execute scripts_file on remote servers.
    '''

    ips_file = './iplists'
    ips_list = get_iplists(ips_file)

    # cmds_file = './cmds'
    # cmds_list = get_iplists(cmds_file)
    # exec_cmds(ips_list, cmds_list)

    bash_file = './' + sys.argv[1]

    start_time = time.time()
    #exec_files(ips_list, bash_file, 'serial')
    exec_files(ips_list, bash_file, 'coroutine')
    #exec_files(ips_list, bash_file, 'multi')
    # exec_files(ips_list, bash_file)
    end_time = time.time()
    print('Script elapsed : %ss.' % (end_time - start_time))


