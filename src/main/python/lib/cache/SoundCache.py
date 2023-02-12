#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# Copyright 2019-2023 Denis Meyer
#
# This file is part of the Wheel of Fun app.
#

'''Wheel of Fun - SoundCache'''

import logging

import pygame

from lib.cache.Cache import Cache


class SoundCache(Cache):

    def __init__(self, appconfig):
        '''Initializes

        :param appconfig: The app config
        '''
        super()

        logging.debug('Initializing SoundCache')

        self.appconfig = appconfig

        self.sound_stopper = None
        self.sound_tada = None
        self.num_channels = 30
        pygame.mixer.set_num_channels(self.num_channels)  # default is 8

        self.curr_channel = 0

        self._load()

    def play(self, sound):
        '''Plays the sound

        :param sound: Sound to play
        '''
        pygame.mixer.Channel(self.curr_channel).play(sound)
        self.curr_channel += 1
        self.curr_channel = self.curr_channel % self.num_channels

    def _load(self):
        '''Loads the sounds'''
        logging.debug('Loading sounds')

        self.sound_stopper = pygame.mixer.Sound(self.appconfig.path_sound_stopper)
        self.sound_tada = pygame.mixer.Sound(self.appconfig.path_sound_tada)
