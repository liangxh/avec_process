# -*- coding: utf-8 -*-
import os


class FileManager(object):
    mode_lang = [
        ('Train', 'DE'),
        ('Devel', 'DE'),
        ('Test', 'DE'),
        ('Test', 'HU'),
    ]

    @classmethod
    def get_keys(cls, mode, lang=None):
        if mode.lower() == 'train':
            mode = 'Train'
            lang = 'DE'
            n = 34
        elif mode.lower() == 'devel':
            mode = 'Devel'
            lang = 'DE'
            n = 14
        elif mode.lower() == 'test' and lang.lower() == 'de':
            mode = 'Test'
            lang = 'DE'
            n = 16
        elif mode.lower() == 'test' and lang.lower() == 'hu':
            mode = 'Test'
            lang = 'HU'
            n = 66
        else:
            raise ValueError('{}_{} not found'.format(mode, lang))

        filenames = ['{}_{}_{:2d}'.format(mode, lang, i) for i in range(1, n + 1)]
        return filenames
