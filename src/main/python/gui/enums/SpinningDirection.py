#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# Copyright 2019-2023 Denis Meyer
#
# This file is part of the Wheel of Fun app.
#

'''Wheel of Fun - SpinningDirection'''

from enum import Enum


class SpinningDirection(Enum):
    LEFT = -1
    NONE = 0
    RIGHT = 1
