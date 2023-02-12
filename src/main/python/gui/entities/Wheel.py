#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# Copyright 2019-2023 Denis Meyer
#
# This file is part of the Wheel of Fun app.
#

'''Wheel of Fun - Wheel'''

import logging
import math
import random

import pygame
from pygame import gfxdraw
from PIL import Image, ImageDraw

from gui.entities.Entity import Entity
import gui.Colors as colors
from gui.Text import Text
from gui.enums.SpinningDirection import SpinningDirection


class Wheel(Entity):

    INCREASE_ON_DRAG = 0.1
    DECREASE_ON_DRAG_STOP = 0.02
    DECREASE_ON_STOPPER_MIN = 0.01
    DECREASE_ON_STOPPER_MAX = 0.04
    THRESHOLD_NOT_SPINNING = 0.01
    MAX_ANGLE_INCREASE = 20

    WHEEL_COLORS = [colors.COLOR_SKYBLUE_2, colors.COLOR_SPRINGGREEN_1, colors.COLOR_LAVENDERBLUSH_4, colors.COLOR_GOLD_1, colors.COLOR_TAN_1,
                    colors.COLOR_CRIMSON, colors.COLOR_MEDIUMORCHID_2, colors.COLOR_SLATEBLUE_1]

    def __init__(self, appconfig, tasks, imagecache, soundcache, size, pos, pos_shift=0):
        '''Initializes

        :param appconfig: The app config
        :param tasks: The tasks
        :param imagecache: The image cache
        :param soundcache: The sound cache
        :param size: Size of the entity
        :param pos: Position of the entity
        :param pos_shift: The position shift of the entity
        '''
        super(Wheel, self)

        logging.debug('Initializing Wheel')

        self.appconfig = appconfig
        self.tasks = tasks
        self.imagecache = imagecache
        self.soundcache = soundcache
        self.pos = pos
        self.size = size
        self.pos_shift = pos_shift

        self.radius = self.size[0] / 2
        self.center = (self.size[0] / 2, self.size[1] / 2)

        self.font = pygame.font.SysFont(self.appconfig.fontname, self.appconfig.fontsize_tasks)
        self.angle = 0
        self.angle_increase = 0
        self.spinning_direction_last = []
        self.spinning_direction = SpinningDirection.NONE

        self.last_mouse_x = self.pos[0]
        self.last_mouse_y = self.pos[0]

        self.surface = pygame.Surface(self.size, pygame.SRCALPHA)
        self.surface.set_colorkey(colors.COLOR_BLACK)

        self.image = self.surface
        self.rect = self.image.get_rect()
        self.rect.center = (pos[0] + self.pos_shift, pos[1] + self.pos_shift)

        self._draw_graphics(self.image)
        self._draw_tasks(self.image)

    def _draw_graphics(self, surface):
        '''Draws the graphical elements

        :param surface: The surface to draw on
        '''
        # Outer
        pygame.gfxdraw.filled_circle(surface, int(self.pos[0]), int(self.pos[1]), int(self.size[0] / 2), colors.COLOR_SGI_GRAY_92)

        # Pie slices
        pil_image = Image.new('RGBA', (self.size[0], self.size[1]))
        start = 0
        step = 45
        end = 45
        band_size = 14
        for sli in range(8):
            pil_draw = ImageDraw.Draw(pil_image)
            pil_draw.pieslice((band_size, band_size, self.size[0] - band_size, self.size[1] - band_size), start, end, fill=self.WHEEL_COLORS[sli])
            mode = pil_image.mode
            size = pil_image.size
            data = pil_image.tobytes()
            image = pygame.image.fromstring(data, size, mode)
            surface.blit(image, (0, 0))
            start = end
            end += step

        inner_circle_radius = 80

        # Inner circle
        gap = 5
        gap_increase = 5
        pygame.gfxdraw.filled_circle(surface, int(self.pos[0]), int(self.pos[1]), inner_circle_radius - gap, colors.COLOR_SGI_GRAY_92)
        gap += gap_increase
        pygame.gfxdraw.filled_circle(surface, int(self.pos[0]), int(self.pos[1]), inner_circle_radius - gap, colors.COLOR_WHITE)

        # Smaller pie slices
        small_size = (132, 132)
        pil_image = Image.new('RGBA', (small_size[0], small_size[1]))
        start = 0
        step = 45
        end = 45
        band_size = 0
        for sli in range(8):
            pil_draw = ImageDraw.Draw(pil_image)
            pil_draw.pieslice((band_size, band_size, small_size[0] - band_size, small_size[1] - band_size), start, end, fill=self.WHEEL_COLORS[sli])
            mode = pil_image.mode
            size = pil_image.size
            data = pil_image.tobytes()
            image = pygame.image.fromstring(data, small_size, mode)
            surface.blit(image, (self.pos[0] - small_size[0] / 2, self.pos[1] - small_size[1] / 2))
            start = end
            end += step

        # Wheel logo
        # TODO: Change logo on MAX_ANGLE_INCREASE
        self.img_wheel_logo = self.imagecache.wheel_logo
        logo_x = int(self.size[0] / 4)
        logo_y = int(self.size[1] / 4)
        self.img_wheel_logo = pygame.transform.scale(self.img_wheel_logo, (logo_x, logo_y))
        surface.blit(self.img_wheel_logo, (self.pos[0] - logo_x / 2, self.pos[1] - logo_y / 2 - 12))

        # Wheel stopper
        wheel_stopper_color = colors.COLOR_SIENNA

        # North
        north_x = int(self.pos[0])
        north_y = 0 + 8
        pygame.draw.circle(surface, wheel_stopper_color, (north_x, north_y), 5, 0)
        # East
        east_x = int(self.pos[0] + self.size[0] / 2) - 7
        east_y = int(self.pos[1])
        pygame.draw.circle(surface, wheel_stopper_color, (east_x, east_y), 5, 0)
        # South
        south_x = int(self.pos[0]) + 1
        south_y = int(self.pos[1] + self.size[1] / 2) - 7
        pygame.draw.circle(surface, wheel_stopper_color, (south_x, south_y), 5, 0)
        # West
        west_x = int(self.pos[0] - self.size[0] / 2) + 7
        west_y = int(self.pos[1]) + 1
        pygame.draw.circle(surface, wheel_stopper_color, (west_x, west_y), 5, 0)

        # Calculation of a point on an arc:
        # Let the coordinates of P1 be (xP1, yP1).
        # Let the angle between the points P1 and P2 be θ.
        # Then from the arc d you get, θ = d / r = 2πx. So, now, we have
        # xP2 = xP1 + r * sinθ
        # yP2 = yP1 − r * (1 − cosθ)

        small_circle_radius = int(5 / 2)

        # North-East
        x1 = north_x + self.radius * math.sin(math.radians(45)) - small_circle_radius - 1
        y1 = north_y + self.radius * (1 - math.cos(math.radians(45))) - 1
        pygame.draw.circle(surface, wheel_stopper_color, (int(x1), int(y1)), 5, 0)
        # South-East
        x1 = east_x - self.radius * (1 - math.sin(math.radians(45))) + small_circle_radius + 1
        y1 = east_y + self.radius * math.cos(math.radians(45)) - small_circle_radius - 2
        pygame.draw.circle(surface, wheel_stopper_color, (int(x1), int(y1)), 5, 0)
        # South-West
        x1 = south_x - self.radius * math.sin(math.radians(45)) + small_circle_radius + 2
        y1 = south_y - self.radius * (1 - math.cos(math.radians(45))) + small_circle_radius + 1
        pygame.draw.circle(surface, wheel_stopper_color, (int(x1), int(y1)), 5, 0)
        # North-West
        x1 = west_x + self.radius * (1 - math.sin(math.radians(45))) - small_circle_radius / 2 + 0
        y1 = west_y - self.radius * math.cos(math.radians(45)) + small_circle_radius + small_circle_radius / 2 + 1
        pygame.draw.circle(surface, wheel_stopper_color, (int(x1), int(y1)), 5, 0)

    def _draw_tasks(self, surface):
        '''Draws all tasks
        
        :param surface: Surface to draw on
        '''
        r = int(self.size[0] / 2 * 3 / 5)
        # Helping circle
        #pygame.gfxdraw.aacircle(surface, int(self.pos[0]), int(self.pos[1]), r, colors.COLOR_SGI_GRAY_92)
        #logging.debug('Circle mid: {}, {}'.format(int(self.pos[0]), int(self.pos[1])))

        angle_degree = 360 / 8
        positions = {}
        for i in range(0, 8):
            _angle_corrected_radians = math.radians(angle_degree * (i + 1) - angle_degree / 2)
            x, y = r * math.cos(_angle_corrected_radians), r * math.sin(_angle_corrected_radians)
            logging.debug('{}. (x, y) = ({}, {})'.format(i, x, y))
            positions[i] = {
                'pos': (self.pos[0] + x, self.pos[1] + y),
                'angle': (-20 - (46 * i))
            }
            logging.debug('Pos(x, y) = ({}, {}), Angle = {}'.format(positions[i]['pos'][0], positions[i]['pos'][1], positions[i]['angle']))
            # Helping dots
            #pygame.gfxdraw.filled_circle(surface, int(positions[i]['pos'][0]), int(positions[i]['pos'][1]), 5, colors.COLOR_CRIMSON)

        for i, task in enumerate(self.tasks.tasks):
            if i < 8:
                tpos = positions[i]['pos']
                angle = positions[i]['angle']
                _task = (task[:(self.appconfig.task_max_length - 3)] + '...') if len(task) > self.appconfig.task_max_length else task
                text = Text(self.appconfig, self.appconfig.size_tasks, tpos, _task, self.appconfig.fontsize_tasks, colors.COLOR_WHITE, rotation_angle=angle)
                text.draw(surface)

    def _update_spinning_direction(self):
        '''Updates the spinning direction'''
        self.spinning_direction_last.append(self.spinning_direction)
        if len(self.spinning_direction_last) > 20:
            self.spinning_direction_last = self.spinning_direction_last[20:]
        if self.angle_increase >= -self.INCREASE_ON_DRAG and self.angle_increase <= self.INCREASE_ON_DRAG:
            self.spinning_direction = SpinningDirection.NONE
        elif self.angle_increase > 0:
            self.spinning_direction = SpinningDirection.RIGHT
        else:
            self.spinning_direction = SpinningDirection.LEFT

    def _update_angle_increase_on_mouse_pressed(self, mouse_x, mouse_y):
        '''Updates the angle increase on mouse pressed'''
        in_left_half = mouse_x <= self.center[0]
        if self.last_mouse_y < mouse_y:
            self.angle_increase += -self.INCREASE_ON_DRAG if in_left_half else self.INCREASE_ON_DRAG
        else:
            self.angle_increase += self.INCREASE_ON_DRAG if in_left_half else -self.INCREASE_ON_DRAG

    def _get_angle_decrease_factor(self):
        '''Returns the angle decrease factor for "smoothing out"

        :return: Angle decrease factor
        '''
        if not self.is_spinning():
            return 1.0

        if self.is_spinning_right():
            if self.angle_increase <= 0.4:
                value = 0.08
            elif self.angle_increase <= 0.5:
                value = 0.09
            elif self.angle_increase <= 0.6:
                value = 0.1
            elif self.angle_increase <= 0.7:
                value = 0.11
            elif self.angle_increase <= 0.8:
                value = 0.125
            elif self.angle_increase <= 0.9:
                value = 0.15
            elif self.angle_increase <= 1:
                value = 0.22
            elif self.angle_increase <= 1.1:
                value = 0.31
            elif self.angle_increase <= 1.2:
                value = 0.4
            elif self.angle_increase <= 1.3:
                value = 0.5
            elif self.angle_increase <= 1.4:
                value = 0.6
            elif self.angle_increase <= 2:
                value = 0.7
            elif self.angle_increase <= 3:
                value = 0.8
            elif self.angle_increase <= 4:
                value = 0.9
            elif self.angle_increase <= 5:
                value = 0.95
            else:
                value = 1
        else:
            if self.angle_increase >= -0.4:
                value = 0.08
            elif self.angle_increase >= -0.5:
                value = 0.09
            elif self.angle_increase >= -0.6:
                value = 0.1
            elif self.angle_increase >= -0.7:
                value = 0.11
            elif self.angle_increase >= -0.8:
                value = 0.125
            elif self.angle_increase >= -0.9:
                value = 0.15
            elif self.angle_increase >= -1:
                value = 0.22
            elif self.angle_increase >= -1.1:
                value = 0.31
            elif self.angle_increase >= -1.2:
                value = 0.4
            elif self.angle_increase >= -1.3:
                value = 0.5
            elif self.angle_increase >= -1.4:
                value = 0.6
            elif self.angle_increase >= -2:
                value = 0.7
            elif self.angle_increase >= -3:
                value = 0.8
            elif self.angle_increase >= -4:
                value = 0.9
            elif self.angle_increase >= -5:
                value = 0.95
            else:
                value = 1

        return value

    def _get_angle_increase(self):
        '''Returns the angle increase value, multiplies a factor for "smoothing out"

        :return: Angle increase value
        '''
        value = self.DECREASE_ON_DRAG_STOP * self._get_angle_decrease_factor()

        return -1 * value if self.is_spinning_right() else value

    def _update_angle_increase_on_mouse_not_pressed(self):
        '''Updates the angle increase on mouse not pressed'''
        self.angle_increase += self._get_angle_increase()

        # Decrease speed every stopper (~= every 45 degrees) a bit more
        if self._is_45_deg():
            factor = 1 if self.is_spinning_right() else -1
            self.angle_increase -= factor * \
                random.uniform(self.DECREASE_ON_STOPPER_MIN, self.DECREASE_ON_STOPPER_MAX)

        # TODO: Spin back on stopper bump

        if self.spinning_direction == SpinningDirection.NONE:
            self.angle_increase = 0
        elif self.spinning_direction == SpinningDirection.RIGHT and self.angle_increase <= self.THRESHOLD_NOT_SPINNING:
            self.angle_increase = 0
        elif self.spinning_direction == SpinningDirection.LEFT and self.angle_increase >= -self.THRESHOLD_NOT_SPINNING:
            self.angle_increase = 0

    def _update_angle_increase(self):
        '''Updates the angle increase'''
        mouse_pressed, _2, _3 = pygame.mouse.get_pressed()
        mouse_x, mouse_y = pygame.mouse.get_pos()

        self._update_spinning_direction()

        if mouse_pressed:
            self._update_angle_increase_on_mouse_pressed(mouse_x, mouse_y)
        else:
            self._update_angle_increase_on_mouse_not_pressed()

        if self.angle_increase > self.MAX_ANGLE_INCREASE:
            self.angle_increase = self.MAX_ANGLE_INCREASE
        if self.angle_increase < -1 * self.MAX_ANGLE_INCREASE:
            self.angle_increase = -1 * self.MAX_ANGLE_INCREASE

        self.last_mouse_x, self.last_mouse_y = mouse_x, mouse_y

    def _update_angle(self):
        '''Updates the angle'''
        self.angle_mod_45 = self.angle % 45
        self.angle -= self.angle_increase
        self.angle = self.angle % 360

    def _is_45_deg(self):
        '''Returns whether wheel is on 45 degrees

        :return: True if wheel is on 45 degrees, False else
        '''
        factor = 1 if self.is_spinning_right() else -1
        incdec = 3 + factor * self.angle_increase
        d1 = False
        d2 = False
        if self.is_spinning_right():
            d1 = self.angle_mod_45 > incdec
            d2 = self.angle_mod_45 - self.angle_increase < incdec
        elif self.is_spinning_left():
            d1 = self.angle_mod_45 < (45 - incdec)
            d2 = self.angle_mod_45 + factor * \
                self.angle_increase > (45 - incdec)
        return d1 and d2

    def _play_sound_stopper(self):
        self.soundcache.play(self.soundcache.sound_stopper)

    def _play_sound_tada(self):
        self.soundcache.play(self.soundcache.sound_tada)

    def is_spinning(self):
        '''Returns whether the wheel is spinning

        :return: True if the wheel is spinning, False else
        '''
        return self.spinning_direction != SpinningDirection.NONE

    def is_spinning_right(self):
        '''Returns whether the wheel is spinning in the right direction

        :return: True if the wheel is spinning in the right direction, False else
        '''
        return self.spinning_direction == SpinningDirection.RIGHT

    def is_spinning_left(self):
        '''Returns whether the wheel is spinning in the left direction

        :return: True if the wheel is spinning in the left direction, False else
        '''
        return self.spinning_direction == SpinningDirection.LEFT

    def get_nr_of_rounds_not_spinning(self):
        '''Returns how many rounds the wheel is not spinning

        :return: How many rounds the wheel is not spinning, if was spinning
        '''
        resting_rounds = 0
        for d in reversed(self.spinning_direction_last):
            if d == SpinningDirection.NONE:
                resting_rounds = resting_rounds + 1
            else:
                return resting_rounds, True

        return resting_rounds, False

    # @Override
    def update(self):
        self._update_angle_increase()
        self.image = pygame.transform.rotozoom(self.surface, self.angle, 1)
        self._update_angle()
        x, y = self.rect.center
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        if self._is_45_deg():
            self._play_sound_stopper()
        rounds_not_spinning, was_spinning = self.get_nr_of_rounds_not_spinning()
        if not self.is_spinning() and was_spinning and rounds_not_spinning > 5:
            self._play_sound_tada()
            self.spinning_direction_last = []

    # @Override
    def draw(self, surface):
        surface.blit(self.image, self.rect)
