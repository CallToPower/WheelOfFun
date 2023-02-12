#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# Copyright 2019-2023 Denis Meyer
#
# This file is part of the Wheel of Fun app.
#

'''Wheel of Fun - Main'''

import logging
import os
import sys
import time
from pathlib import Path

from lib.AppConfig import AppConfig
from gui.GUI import GUI


# Logging configuration
log_to_file = False
logging_loglevel = logging.INFO
logging_datefmt = '%d-%m-%Y %H:%M:%S'
logging_format = '[%(asctime)s] [%(levelname)-5s] [%(module)-20s:%(lineno)-4s] %(message)s'
logging_logfile = str(Path.home()) + '/logs/wheeloffun.application-' + time.strftime('%d-%m-%Y-%H-%M-%S') + '.log'

def _initialize_logger():
    '''Initializes the logger'''
    logging.basicConfig(level=logging_loglevel,
                        format='[%(asctime)s] [%(levelname)-5s] [%(module)-20s:%(lineno)-4s] %(message)s',
                        datefmt='%d-%m-%Y %H:%M:%S')

    if log_to_file:
        basedir = os.path.dirname(logging_logfile)

        if not os.path.exists(basedir):
            os.makedirs(basedir)

        handler_file = logging.FileHandler(logging_logfile, mode='w', encoding=None, delay=False)
        handler_file.setLevel(logging_loglevel)
        handler_file.setFormatter(logging.Formatter(fmt=logging_format, datefmt=logging_datefmt))
        logging.getLogger().addHandler(handler_file)

if __name__ == '__main__':
    _initialize_logger()
    logging.debug('Starting')

    appconfig = AppConfig()

    gui = GUI(appconfig)
    gui.read_tasks()
    gui.run()
