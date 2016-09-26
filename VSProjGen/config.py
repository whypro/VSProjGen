# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import os


class Config(object):
    ext_exclude = [
        '.d',
        '.o',
        '.tdr',
    ]
    dir_exclude = [
        'shadow',
        'tools',
        'dep',
        'lib',
        '.git',
        '.svn',
    ]
    src_path = 'E:\\SHServerSource\\sync\\shs\\src'
    output_path = '.\\output'
    solution_name = 'T7'
