import os


class Ping(object):

    def run(self):
        with os.popen("ping -c1 127.0.0.1", "r") as ping_rslt:
            for lines in ping_rslt:
                print(lines.strip())

