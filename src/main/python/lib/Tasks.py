#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# Copyright 2019-2023 Denis Meyer
#
# This file is part of the Wheel of Fun app.
#

'''Wheel of Fun - Tasks'''

import logging
import random


class Tasks:
    '''The tasks reader'''

    def __init__(self, appconfig):
        '''Initializes the tasks reader

        :param appconfig: The application config
        '''
        logging.debug('Initializing Tasks')

        self.appconfig = appconfig

        self.tasks = []

        self._init()

    def save_tasks(self, tasks):
        '''Sets new tasks

        :param tasks: The new tasks
        '''
        if not self.appconfig.tasksFilePath:
            return

        with open(self.appconfig.tasksFilePath, 'w') as f:
            f.write('# One line per task\n')
            for t in tasks:
                f.write(t)
                f.write('\n')
        self._init()

    def _init(self):
        '''Reads in the file and parses the tasks'''
        self.tasks = []

        if not self.appconfig.tasksFilePath:
            return

        try:
            with open(self.appconfig.tasksFilePath, 'r') as f:
                for line in f:
                    _line = line.strip()
                    if _line and not _line.startswith('#'):
                        self.tasks.append(_line)
            if self.appconfig.randomize_tasks:
                random.shuffle(self.tasks)
        except Exception as e:
            logging.error('Error loading file "{}: {}"'.format(self.appconfig.tasksFilePath, e))
