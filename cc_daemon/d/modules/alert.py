import os


class Alert(object):

    def run(self):
        with os.popen("echo ERROR!", "r") as rslt:
            for lines in rslt:
                print(lines.strip())

