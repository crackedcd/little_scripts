import os
import d.modules.actions.log


class Alert2(object):

    def __init__(self):
        l = d.modules.actions.log.Log("alert2")
        l.log()

    def run(self):
        with os.popen("echo WARNNING!", "r") as rslt:
            for lines in rslt:
                print(lines.strip())

