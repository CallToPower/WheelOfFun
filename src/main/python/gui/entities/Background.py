#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# Copyright 2019-2023 Denis Meyer
#
# This file is part of the Wheel of Fun app.
#

'''Wheel of Fun - Background'''

import logging

import pygame
from PIL import Image, ImageDraw

from gui.entities.Entity import Entity


class Background(Entity):

    def __init__(self, appconfig, imagecache, pos, display_image=False):
        '''Initializes

        :param appconfig: The app config
        :param imagecache: The image cache
        :param pos: Position of the entity
        :param display_image: Whether to display an image or a plain background
        '''
        super(Background, self)

        logging.debug('Initializing Background')

        self.appconfig = appconfig
        self.imagecache = imagecache
        self.display_image = display_image

        self.size = self.appconfig.screen_size

        self.bgimg = self.imagecache.background
        self.image = pygame.transform.scale(self.bgimg, self.appconfig.screen_size)
        self.rect = self.image.get_rect()
        self.rect.center = pos

    # @Override
    def draw(self, surface):
        if self.display_image:
            surface.blit(self.image, self.rect)
        else:
            surface.fill(self.appconfig.bg_color)
