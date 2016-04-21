#!/usr/bin/python
# coding: utf-8

import os
import sys
import time
import datetime
from pprint import pprint

import d.modules.actions.log


class CMQMonitor(object):

    def __init__(self):

        l = d.modules.actions.log.Log("cmq_monitor")
        l.log()

        self.__cmq_path = "/data/cft_msg_queue/"
        self.__proxy_path = self.__cmq_path + "/proxy/"
        self.__worker_path = self.__cmq_path + "/worker/"
        self.__log_path = self.__cmq_path + "/log/"
        self.__time_now = datetime.datetime.now().strftime("%Y%m%d%H%M%S")
        self.__log_file = self.__log_path + "/logfile_" + self.__time_now + ".log"
        self.__proxy_statis_file = self.__proxy_path + "/bin/asyn_msg_statis"
        self.__worker_statis_file = self.__worker_path + "/bin/asyn_msg_statis"
        self.__last_value_file = self.__log_path + "/last_value_file"

        self.__proxy_monitor_script = self.__proxy_path + "/bin/monitor_proxy.sh"
        self.__worker_monitor_script = self.__worker_path + "/bin/monitor_worker.sh"
        self.__worker_chk_disk_script = self.__worker_path + "/bin/chk_disk.sh"
        self.__worker_backup_msg_script = self.__worker_path + "/bin/backup_msg.sh"

        self.__alarm_server_ip = "172.27.31.197"
        self.__alarm_server_port = "61616"
        self.__alarm_data_name = "mqcenter_data"  # 这里写死, 所有上报数据都一致, 不要根据业务改变
        self.__alarm_data_type = "8"  # "业务特性"类型是8, "接口"类型是20, "错误码"类型是22.
        self.__statis_file_line_length = 9  # 统计文件的行长度是9, 如果超过9, 说明有"消费者名称"列, 是一个worker.

        self.__exec_log = self.__log_path + "/exec_" + self.__time_now + ".log"

    def run(self):
        print(datetime.datetime.now())
        print("---------------------")
        self.__init()
        my_type = self.__server_type()
        self.__process_monitor(my_type)
        self.__send_data(my_type, self.__load_last_value(self.__last_value_file))
        self.__housekeeper(self.__log_path)

    def __server_type(self):
        if os.path.exists(self.__proxy_path):
            return "proxy"
        elif os.path.exists(self.__worker_path):
            return "worker"
        else:
            sys.exit()


    def __init(self):
        # make log dir.
        if not os.path.isdir(self.__log_path):
            os.mkdir(self.__log_path)


    def __clean_last_value_file(self, last_value_value):
        # initial self.__last_value_file.
        os.system("> " + self.__last_value_file)


    def __housekeeper(self, hk_path):
        cmq_log_path = self.__cmq_path + "/" + self.__server_type() + "/log/"
        os.system("/usr/bin/find " + hk_path  + " -type f -mtime +3 -delete")
        os.system("/usr/bin/find " + cmq_log_path  + " -type f -mtime +7 -delete")


    def __process_monitor(self, monitor_type):
        restart_script_path = self.__cmq_path + "/" + monitor_type + "/bin/"
        os.system("chmod a+x " + restart_script_path + "/*.py")
        os.system("chmod a+x " + restart_script_path + "/*.sh")
        os.system("/bin/date >> " + self.__exec_log)
        # if this is a cmq proxy server.
        if monitor_type == "proxy":
            os.system("/bin/bash " + self.__proxy_monitor_script + " 2>&1 >> " + self.__exec_log + " &")

        # if this is a cmq worker server.
        if monitor_type == "worker":
            os.system("/bin/bash " + self.__worker_monitor_script + " 2>&1 >> " + self.__exec_log + " &")
            os.system("/bin/bash " + self.__worker_chk_disk_script + " 2>&1 >> " + self.__exec_log + " &")
            # cmq backup msg data files at 05:34 a.m.
            backup_time = "0534"
            if datetime.datetime.now().strftime("%H%M") == backup_time:
                os.system("/bin/bash " + self.__worker_backup_msg_script + " 2>&1 >> " + self.__exec_log + " &")


    def __send_data(self, monitor_type, last_data):

        statis_file = self.__cmq_path + "/" + monitor_type + "/bin/asyn_msg_statis"

        if monitor_type == "proxy":
            monitor_tag = "cmq_proxy"
            ## 已处理消息数: 队列消息入/出一次合计一个已处理, 一直累加.
            total_msg_code = 98665
            ## 正处理消息数: 队列已发送出的消息, 但尚未收到ack.
            acc_msg_code = 98666
            ## 待处理消息数: 队列从预读文件中预估的需要处理的消息数.
            unacc_msg_code = 98667
            ## 错误消息文件中消息数: 处理失败的消息数.
            err_msg_code = 98668

        elif monitor_type == "worker":
            monitor_tag = "cmq_worker"
            ## 已处理消息数: 队列消息入/出一次合计一个已处理, 一直累加.
            total_msg_code = 98672
            ## 正处理消息数: 队列已发送出的消息, 但尚未收到ack.
            acc_msg_code = 98673
            ## 待处理消息数: 队列从预读文件中预估的需要处理的消息数.
            unacc_msg_code = 98674
            ## 错误消息文件中消息数: 处理失败的消息数.
            err_msg_code = 98675

        # clean last value data.
        self.__clean_last_value_file(self.__last_value_file)

        with open(statis_file) as fd:
            for lines in fd.readlines():
                line = lines.strip("\n").split("|")
                # 时间
                statis_time = line[0]
                # ip
                ip = line[1]
                # 队列名
                topic = line[2]
                # 文件名
                msg_file = line[3]
                # 偏移量
                offset = line[4]
                # 已处理消息总数
                total_msg = line[5]
                # 正在处理消息数
                acc_msg = line[6]
                # 未处理消息数
                unacc_msg = line[7]
                # 错误消息数
                err_msg = line[8]
                # 消费者名称
                if (len(line) > self.__statis_file_line_length) and (type == "worker"):
                    # worker的消费者是订阅方
                    consumer_name = line[9].split("-")[0]
                else:
                    # proxy没有消费者, 把proxy的消费者当成是worker, 即cmq_server
                    consumer_name = "cmq_server"

                # send infomations to mon.cf.com
                #print "/data/cftlogagent/bin/sendinfo %s %s %s %s \"%s#%s|%s|%s|%s|%s|%s|||\"" % (ip, self.__alarm_server_ip, self.__alarm_server_port, self.__alarm_data_name, self.__alarm_data_type, monitor_tag, statis_time, total_msg_code, total_msg, topic, ip)
                #print "/data/cftlogagent/bin/sendinfo %s %s %s %s \"%s#%s|%s|%s|%s|%s|%s|||\"" % (ip, self.__alarm_server_ip, self.__alarm_server_port, self.__alarm_data_name, self.__alarm_data_type, monitor_tag, statis_time, acc_msg_code, acc_msg, topic, ip)
                #print "/data/cftlogagent/bin/sendinfo %s %s %s %s \"%s#%s|%s|%s|%s|%s|%s|||\"" % (ip, self.__alarm_server_ip, self.__alarm_server_port, self.__alarm_data_name, self.__alarm_data_type, monitor_tag, statis_time, unacc_msg_code, unacc_msg, topic, ip)
                #print "/data/cftlogagent/bin/sendinfo %s %s %s %s \"%s#%s|%s|%s|%s|%s|%s|||\"" % (ip, self.__alarm_server_ip, self.__alarm_server_port, self.__alarm_data_name, self.__alarm_data_type, monitor_tag, statis_time, err_msg_code, err_msg, topic, ip)

                os.system("echo " + "%s-%s %s %s %s %s" % (topic, consumer_name, total_msg, acc_msg, unacc_msg, err_msg) + " >> " + self.__last_value_file)

                uniq_key = topic + "-" + consumer_name
                if uniq_key in last_data:
                    last_total_msg = last_data[uniq_key][0]
                    last_acc_msg = last_data[uniq_key][1]
                    last_unacc_msg = last_data[uniq_key][2]
                    last_err_msg = last_data[uniq_key][3]

                    os.system("/data/cftlogagent/bin/sendinfo %s %s %s %s \"%s#%s|%s|%s|%s|%s|%s|%s||\"" % (ip, self.__alarm_server_ip, self.__alarm_server_port, self.__alarm_data_name, self.__alarm_data_type, monitor_tag, statis_time, total_msg_code, self.__between_result(total_msg, last_total_msg), topic, ip, consumer_name) + " >> " + self.__log_file)
                    os.system("/data/cftlogagent/bin/sendinfo %s %s %s %s \"%s#%s|%s|%s|%s|%s|%s|%s||\"" % (ip, self.__alarm_server_ip, self.__alarm_server_port, self.__alarm_data_name, self.__alarm_data_type, monitor_tag, statis_time, acc_msg_code, int(acc_msg), topic, ip, consumer_name) + " >> " + self.__log_file)
                    os.system("/data/cftlogagent/bin/sendinfo %s %s %s %s \"%s#%s|%s|%s|%s|%s|%s|%s||\"" % (ip, self.__alarm_server_ip, self.__alarm_server_port, self.__alarm_data_name, self.__alarm_data_type, monitor_tag, statis_time, unacc_msg_code, int(unacc_msg), topic, ip, consumer_name) + " >> " + self.__log_file)
                    os.system("/data/cftlogagent/bin/sendinfo %s %s %s %s \"%s#%s|%s|%s|%s|%s|%s|%s||\"" % (ip, self.__alarm_server_ip, self.__alarm_server_port, self.__alarm_data_name, self.__alarm_data_type, monitor_tag, statis_time, err_msg_code, int(err_msg), topic, ip, consumer_name) + " >> " + self.__log_file)


    #between_result = lambda x, y: (int(x) - int(y)) if int(x) > int(y) else 0
    def __between_result(self, x, y):
        if int(x) > int(y):
            return int(x) - int(y)
        else:
            return 0


    def __load_last_value(self, last_value_file):
        last_data = {}
        os.system("touch " + last_value_file)
        with open(self.__last_value_file) as fd:
            for lines in fd:
                line_data = []
                line = lines.strip("\n").split(" ")
                last_data[line[0]] = []
                last_data[line[0]].append(line[1])
                last_data[line[0]].append(line[2])
                last_data[line[0]].append(line[3])
                last_data[line[0]].append(line[4])
        return last_data

