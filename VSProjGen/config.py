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
   
    # 源代码目录
    # src_path = 'E:\\SHServerSource\\sync\\shs\\src'
    src_path = 'Z:\\sync\\shs\\src'
    # 解决方案自动生成目录
    output_path = 'T7'
    # 解决方案名称
    solution_name = 'T7'
    # 是否为单工程，True 则对于源代码目录中的每个子目录建立工程文件，False 则将所有目录加入同一个工程
    single_project = False

    #src_path = 'C:\\Users\\haoyuwang\\Desktop\\Open Source\\Libevent'
    #output_path = 'E:\\Visual Studio 2015\\Projects\\Libevent'
    #solution_name = 'Libevent'
    #single_project = True
