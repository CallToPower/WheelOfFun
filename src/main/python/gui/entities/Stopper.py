#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# Copyright 2019-2023 Denis Meyer
#
# This file is part of the Wheel of Fun app.
#

'''Wheel of Fun - Stopper'''

import logging

import pygame
import gui.Colors as colors
from PIL import Image, ImageDraw

from gui.entities.Entity import Entity


class Stopper(Entity):

    def __init__(self, appconfig, imagecache, pos):
        '''Initializes

        :param appconfig: The app config
        :param imagecache: The image cache
        :param pos: Position of the entity
        '''
        super(Stopper, self)

        logging.debug('Initializing Stopper')

        self.appconfig = appconfig
        self.imagecache = imagecache
        self.pos = pos
        self.size = (150, 300)

        self.surface = pygame.Surface(self.size)
        self.surface.fill(colors.COLOR_WHITE)
        self.surface.set_colorkey(colors.COLOR_WHITE)

        self.image = self.surface
        self.rect = self.image.get_rect()
        self.rect.center = pos

        self._draw_graphics(self.image)

    def _draw_graphics(self, surface):
        '''Draws the graphical elements

        :param surface: The surface to draw on
        '''
        pygame.draw.polygon(surface, colors.COLOR_SGI_GRAY_92, [[0, 0], [self.size[0], 0], [self.size[0] / 2, self.size[1]]], 0)
        gap = 3
        factor = 1
        pygame.draw.polygon(surface, colors.COLOR_SGI_GRAY_76, [[gap * factor, 0], [self.size[0] - gap * factor, 0], [self.size[0] / 2, self.size[1] - gap * factor]], 0)
        factor += 1
        pygame.draw.polygon(surface, colors.COLOR_SGI_GRAY_56, [[gap * factor, 0], [self.size[0] - gap * factor, 0], [self.size[0] / 2, self.size[1] - gap * factor]], 0)
        factor += 1
        pygame.draw.polygon(surface, colors.COLOR_SGI_GRAY_36, [[gap * factor, 0], [self.size[0] - gap * factor, 0], [self.size[0] / 2, self.size[1] - gap * factor]], 0)
        factor += 1
        pygame.draw.polygon(surface, colors.COLOR_SGI_GRAY_16, [[gap * factor, 0], [self.size[0] - gap * factor, 0], [self.size[0] / 2, self.size[1] - gap * factor]], 0)
        factor += 1
        pygame.draw.polygon(surface, colors.COLOR_BLACK, [[gap * factor, 0], [self.size[0] - gap * factor, 0], [self.size[0] / 2, self.size[1] - gap * factor]], 0)

    # @Override
    def draw(self, surface):
        '''Draws the wheel

        :param surface: The surface to draw on
        '''
        surface.blit(self.image, self.rect)
