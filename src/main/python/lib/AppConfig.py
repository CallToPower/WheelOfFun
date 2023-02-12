#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# Copyright 2019-2023 Denis Meyer
#
# This file is part of the Wheel of Fun app.
#

'''Wheel of Fun - AppConfig'''

import logging
import os

from lib.I18n import I18n
import gui.Colors as colors


class AppConfig:
    '''The application configuration'''

    def __init__(self):
        '''Initialization'''

        home_dir = os.path.expanduser("~")
        wof_dir = '{}/{}'.format(home_dir, 'wheeloffun')
        if not os.path.exists(wof_dir):
            os.makedirs(wof_dir)
        self.tasksFilePath = '{}/tasks.wfn'.format(wof_dir)

        self.i18n = I18n(language='deDe')

        self.fontname = 'Comic Sans Ms'

        self.fontsize_tasks = 12
        self.task_max_length = 38

        self.size_tasks = (80, 80)

        self.path_img_app_logo = 'resources/base/app-logo.png'
        self.path_img_wheel_logo = 'resources/base/wheel-logo.png'
        self.path_img_background = 'resources/base/background.jpeg'

        self.path_sound_stopper = 'resources/base/stopper.wav'
        self.path_sound_tada = 'resources/base/tada.wav'

        self.bg_color = colors.COLOR_BLACK
        self.display_bg_image = True

        self.randomize_tasks = False

        self.screen_size = (800, 800)
        self.fps = 60
