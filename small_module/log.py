#!/usr/bin/env python
# coding: utf-8

import logging

class LOG:

    def main(self):
        ## log to file
        #logging.basicConfig(filename="example.log", format="%(asctime)s %(levelname)s:%(message)s", datefmt="%Y/%m/%d %H:%M:%S", level=logging.DEBUG)
        #logging.debug('This message should go to the log file as the log level is DEBUG')
        #logging.info('So should this')
        #logging.warning('And this, too')

        ## log to output
        my_module_logger = logging.getLogger('my_module')
        my_module_logger.setLevel(logging.DEBUG)
        sh = logging.StreamHandler()
        sh.setLevel(logging.DEBUG)
        formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
        sh.setFormatter(formatter)
        my_module_logger.addHandler(sh)
        my_module_logger.debug('debug message')
        my_module_logger.info('info message')
        my_module_logger.warn('warn message')
        my_module_logger.error('error message')
        my_module_logger.critical('critical message')


if __name__ == "__main__":
    l = LOG()
    l.main()

