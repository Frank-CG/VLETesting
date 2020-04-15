#!/usr/bin/env python3
import logging
import os
import datetime
from constant import LOG_DIR

# create log dir
if not os.path.exists(LOG_DIR):
    os.makedirs(LOG_DIR)

# get log file name
LOG_FILE = LOG_DIR + "log" + '-' + datetime.datetime.today().strftime('%Y%m%d-%H%M%S') + '.log'
print("Log file: " + LOG_FILE)


class Logger:
    def __init__(self, file=None):
        if file is None:
            self.file = __name__
        else:
            self.file = file
        # create logger
        self.logger = logging.getLogger(self.file)
        self.logger.setLevel(logging.INFO)

        # create file handler which logs even debug messages
        fh = logging.FileHandler(LOG_FILE)
        fh.setLevel(logging.INFO)

        # create console handler with a higher log level
        ch = logging.StreamHandler()
        ch.setLevel(logging.WARNING)

        # create formatter and add it to the handlers
        # formatter_fh = logging.Formatter('%(asctime)s - %(filename)s - %(levelname)s - %(message)s', datefmt="%H:%M:%S-%f")
        formatter_fh = logging.Formatter('%(asctime)s - %(filename)s - %(levelname)s - %(message)s')
        fh.setFormatter(formatter_fh)
        formatter_ch = logging.Formatter('%(asctime)s - %(filename)s - %(message)s')
        ch.setFormatter(formatter_ch)

        # add the handlers to the logger
        self.logger.addHandler(fh)
        self.logger.addHandler(ch)

    def get(self):
        return self.logger


logger = Logger().get()

def get_logger():
    return logger
