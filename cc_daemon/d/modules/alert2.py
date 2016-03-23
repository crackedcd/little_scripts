import os


class Alert2(object):

    def run(self):
        with os.popen("echo WARNNING!", "r") as rslt:
            for lines in rslt:
                print(lines.strip())

