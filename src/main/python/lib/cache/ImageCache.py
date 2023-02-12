#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# Copyright 2019-2023 Denis Meyer
#
# This file is part of the Wheel of Fun app.
#

'''Wheel of Fun - ImageCache'''

import logging

import pygame

from lib.cache.Cache import Cache


class ImageCache(Cache):

    def __init__(self, appconfig):
        '''Initializes

        :param appconfig: The app config
        '''
        super()

        logging.debug('Initializing ImageCache')

        self.appconfig = appconfig

        self.app_logo = None
        self.wheel_logo = None
        self.background = None

        self._load()

    def _load(self):
        '''Loads the images'''
        logging.debug('Loading images')

        self.app_logo = pygame.image.load(
            self.appconfig.path_img_app_logo).convert()
        self.wheel_logo = pygame.image.load(
            self.appconfig.path_img_wheel_logo).convert_alpha()
        self.background = pygame.image.load(
            self.appconfig.path_img_background).convert()
