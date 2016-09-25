# -*- coding: utf-8 -*-
from __future__ import unicode_literals

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
    # src_path = 'E:\\SHServerSource\\sync\\shs\\src'
    src_path = 'E:\\Codes\\My Github\\Conan'
    output_path = '.\\output1'
    solution_name = 'T7'
