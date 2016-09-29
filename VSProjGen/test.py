# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from . import GroupMap, File, Project, TemplateRender, Solution, Project


__author__  = 'haoyuwang'
__date__ = '2016-09-29'


class Test(object):
    def test_group_map(self):
        print GroupMap.get('.c')
        print GroupMap.get('.h')
        print GroupMap.get('.mk')


    def test_file(self):
        f = File('ai\\ai_stat\\sync_ai_def.h')
        print f.__dict__

    def test_project(self):
        p = Project('sync')
        f = File('ai\\ai_stat\\sync_ai_def.h')
        p.add_file(f)
        f = File('ai\\ai_stat\\sync_ai_def.h')
        p.add_file(f)
        # print p.files
        print p.__dict__
        tr = TemplateRender()
        p.export(tr)

    def test_solution(self):
        s = Solution('T7')
        p = Project('sync')
        f = File('ai\\ai_stat\\sync_ai_def.h')
        p.add_file(f)
        f = File('ai\\ai_stat\\sync_ai_def.h')
        p.add_file(f)
        s.add_project(p)
        tr = TemplateRender(self)
        s.export(tr)
