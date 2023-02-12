#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# Copyright 2019-2023 Denis Meyer
#
# This file is part of the Wheel of Fun app.
#

'''Wheel of Fun - Text'''

import logging

import pygame


class Text():

    def __init__(self, appconfig, size, pos, text, fontsize, color, rotation_angle=0):
        '''Initializes

        :param appconfig: The app config
        :param size: Size of the entity
        :param pos: Position of the entity
        :param text: The text
        :param fontsize: The Fontsize
        :param color: The Color
        :param rotation_angle: Rotation angle
        '''
        super(Text, self).__init__()

        logging.debug('Initializing Text')

        self.appconfig = appconfig
        self.size = size
        self.pos = pos
        self.text = text
        self.fontsize = fontsize
        self.color = color
        self.rotation_angle = rotation_angle

        self.font = pygame.font.SysFont(self.appconfig.fontname, self.fontsize)

    def _rotate(self, surface, angle, pivot, offset):
        """Rotate the surface around a pivot point

        Args:
            surface (pygame.Surface): The surface that is to be rotated
            angle (float): Rotation angle
            pivot (tuple, list, pygame.math.Vector2): The pivot point
            offset (pygame.math.Vector2): Offset vector that is added to the pivot point
        """
        rotated_image = pygame.transform.rotozoom(surface, angle, 1)
        rotated_offset = offset.rotate(angle)
        rect = rotated_image.get_rect(center=pivot+rotated_offset)
        return rotated_image, rect

    def _draw_text(self, surface, font, x, y, text, color):
        '''Draws text

        :param surface: The surface to draw on
        :param font: The font
        :param x: X coordinate
        :param y: Y coordinate
        :param text: The text
        :param color: The text color
        '''
        text_rect = surface.get_rect()
        ftext = font.render(text, True, color)

        pivot = pygame.math.Vector2(self.pos[0], self.pos[1])
        offset = pygame.math.Vector2(0, 0)
        rotated_image, rect = self._rotate(ftext, self.rotation_angle, pivot, offset)

        surface.blit(rotated_image, rect)

    def update(self):
        '''Updates the entity'''
        pass

    def draw(self, surface):
        '''Draws the wheel

        :param surface: The surface to draw on
        '''
        self._draw_text(surface, self.font, self.pos[0], self.pos[1], self.text, self.color)
