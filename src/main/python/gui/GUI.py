#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# Copyright 2019-2023 Denis Meyer
#
# This file is part of the Wheel of Fun app.
#

'''Wheel of Fun - GUI'''

import logging

import pygame

import tkinter as tk
from tkinter import *

import gui.Colors as colors
from lib.cache.ImageCache import ImageCache
from lib.cache.SoundCache import SoundCache
from gui.entities.Background import Background
from gui.entities.Stopper import Stopper
from gui.entities.Wheel import Wheel
from gui.Text import Text
from lib.Tasks import Tasks


class GUI():
    '''Main GUI'''

    SPACEBAR = 32
    # pygame.MOUSEBUTTONDOWN
    # event.button: MOUSEBUTTONDOWN_LEFT = 1
    # event.button: MOUSEBUTTONDOWN_RIGHT = 3

    def __init__(self, appconfig):
        '''Initializes the GUI

        :param appconfig: The app config
        '''
        logging.debug('Initializing GUI')

        self.appconfig = appconfig
        self.imagecache = None
        self.screen = None
        self.screen_mid = (0, 0)
        self.entities = []
        self.wheel = None

        self.rootTk = tk.Tk()
        self.entry_texts = []

        self.tasks = Tasks(self.appconfig)

    def _done_reading(self):
        tasks = [et.get() for et in self.entry_texts]
        self.tasks.save_tasks(tasks)
        self.rootTk.destroy()
        self.rootTk.quit()

    def read_tasks(self):
        '''Reads the tasks'''
        logging.info('Reading tasks')

        self.rootTk.protocol('WM_DELETE_WINDOW', self._done_reading)
        self.rootTk.title(self.appconfig.i18n.get('APP.NAME'))
        row = 0
        for i in range(0, 8):
            Label(self.rootTk, text='Task #{}:\t'.format(i + 1)).grid(row=row)
            entry_text = tk.StringVar()
            e = Entry(self.rootTk, textvariable=entry_text)
            if len(self.tasks.tasks) > i:
                entry_text.set(self.tasks.tasks[i])
            else:
                entry_text.set('')
            self.entry_texts.append(entry_text)
            e.grid(row=row, column=1)
            row = row + 1
        Button(self.rootTk, text=self.appconfig.i18n.get('BUTTON.TASKS.OK'), command=self._done_reading).grid(row=row, column=0, sticky=W, pady=4)
        self.rootTk.mainloop()


    def run(self):
        '''Game loop'''
        logging.info('Starting game loop')

        self._init()

        clock = pygame.time.Clock()
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

            for entity in self.entities:
                entity.update()

            for entity in self.entities:
                entity.draw(self.screen)

            pygame.display.update()

            clock.tick(self.appconfig.fps)

        pygame.quit()

    def _init(self):
        '''Initializes internally'''
        logging.debug('Initializing internally')

        self._init_pygame()
        self._init_entities()

    def _init_pygame(self):
        '''Initializes the game'''
        logging.debug('Initializing pygame')

        pygame.init()
        self.screen = pygame.display.set_mode(self.appconfig.screen_size)

        self.imagecache = ImageCache(self.appconfig)
        self.soundcache = SoundCache(self.appconfig)

        self.screen_mid = (self.appconfig.screen_size[0] / 2, self.appconfig.screen_size[1] / 2)

        pygame.display.set_icon(self.imagecache.app_logo)
        pygame.display.set_caption(self.appconfig.i18n.get('APP.NAME'))

    def _init_entities(self):
        '''Initializes the entities'''
        logging.debug('Initializing entities')

        self.background = Background(self.appconfig, self.imagecache, pos=self.screen_mid, display_image=self.appconfig.display_bg_image)
        pos_shift = 50
        size_wheel_x = self.appconfig.screen_size[0] - pos_shift * 2
        size_wheel_y = self.appconfig.screen_size[1] - pos_shift * 2
        wheel_mid = (size_wheel_x / 2, size_wheel_y / 2)
        self.wheel = Wheel(self.appconfig, self.tasks, self.imagecache, self.soundcache, (size_wheel_x, size_wheel_y), (wheel_mid[0], wheel_mid[1]), pos_shift)
        self.stopper = Stopper(self.appconfig, self.imagecache, pos=(self.screen_mid[0], 0))

        self.entities.append(self.background)
        self.entities.append(self.wheel)
        self.entities.append(self.stopper)
