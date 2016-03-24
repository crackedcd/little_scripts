import os
import d.modules.actions.log


class Alert(object):

    def __init__(self):
        l = d.modules.actions.log.Log("alert")
        l.log()

    def run(self):
        with os.popen("echo ERROR!", "r") as rslt:
            for lines in rslt:
                print(lines.strip())

