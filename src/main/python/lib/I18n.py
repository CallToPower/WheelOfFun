#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# Copyright 2019-2023 Denis Meyer
#
# This file is part of the Wheel of Fun app.
#

'''Wheel of Fun - I18n'''

import logging


class I18n:
    '''The internationalization'''

    _translations_deDe = {
        'APP.NAME': 'Wheel of Fun',
        'BUTTON.TASKS.OK': 'Ok'
    }

    _translations_enUs = {
        'APP.NAME': 'Wheel of Fun',
        'BUTTON.TASKS.OK': 'Ok'
    }

    def __init__(self, language='enUs'):
        '''Initializes I18n

        :param language: The translation language
        '''
        self.language = language
        if self.language.lower().startswith('de'):
            logging.debug('Setting language to deDe')
            self.translations = self._translations_deDe
        else:
            logging.debug('Setting language to enUs')
            self.translations = self._translations_enUs

    def get(self, key, default=None):
        '''Returns the value for the given key or - if not found - a default value

        :param key: The key to be translated
        :param default: The default if no value could be found for the key
        '''
        try:
            return self.translations[key]
        except KeyError as exception:
            logging.error(
                'Returning default for key \'{}\': {}'.format(key, exception))
            if default:
                return default
            else:
                return key
