#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# Copyright 2019-2023 Denis Meyer
#
# This file is part of the Wheel of Fun app.
#

'''Wheel of Fun - Entity'''

import logging

import pygame


class Entity(pygame.sprite.Sprite):

    def __init__(self):
        '''Initializes the entity'''
        super(Entity, self)

    def update(self):
        '''Updates the entity'''
        pass

    def draw(self, surface):
        '''Draws the entity

        :param surface: The surface to draw on
        '''
        pass
