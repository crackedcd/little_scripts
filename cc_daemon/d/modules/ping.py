import os
import d.modules.actions.log


class Ping(object):

    def __init__(self):
        l = d.modules.actions.log.Log("ping")
        l.log()

    def run(self):
        with os.popen("ping -c1 127.0.0.1", "r") as rslt:
            for lines in rslt:
                print(lines.strip())

