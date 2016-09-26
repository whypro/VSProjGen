# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import os
import uuid
from collections import defaultdict

from jinja2 import Environment, Template, FileSystemLoader
import scandir

from .config import Config


config = Config()


class TemplateRender(object):

    def __init__(self):
        self.environment = Environment(loader=FileSystemLoader('template'))

    def render(self, template_name, **kwargs):
        template = self.environment.get_template(template_name)
        return template.render(**kwargs)


class Solution(object):

    def __init__(self, name):
        self.name = name
        self.projects = set()

    def add_project(self, project_obj):
        if project_obj not in self.projects:
            self.projects.add(project_obj)

    def export(self, template_render, output_path):
        if not os.path.exists(output_path):
            os.makedirs(output_path)

        content = template_render.render('sln.template', solution=self)
        export_path = os.path.join(output_path, self.name+'.sln')
        with open(export_path, 'w') as f:
            f.write(content.encode('utf-8'))

        for project in self.projects:
            project.export(template_render, output_path)


class Project(object):

    def __init__(self, name):
        self.name = name
        self.files = set()
        self.groups = set()
        self.filters = set()
        self.guid = '{' + str(uuid.uuid4()) + '}'

    def add_file(self, file_obj, root_dir=False):
        if file_obj not in self.files:
            if root_dir:
                file_obj.abs_path = os.path.join(config.src_path, file_obj.path)
            else:
                file_obj.abs_path = os.path.join(config.src_path, self.name, file_obj.path)

            self.files.add(file_obj)
            group = Group(file_obj.group_name)
            self.groups.add(group)
            if file_obj.filter_name:
                filter = Filter(file_obj.filter_name)
                self.filters.add(filter)

    def export(self, template_render, output_path):
        if not os.path.exists(output_path):
            os.makedirs(output_path)

        content = template_render.render('vcxproj.template', project=self)
        export_path = os.path.join(output_path, self.name+'.vcxproj')
        with open(export_path, 'w') as f:
            f.write(content.encode('utf-8'))

        content = template_render.render('vcxproj.filters.template', project=self)
        export_path = os.path.join(output_path, self.name+'.vcxproj.filters')
        with open(export_path, 'w') as f:
            f.write(content.encode('utf-8'))


class Filter(object):

    def __init__(self, name):
        self.name = name
        self.guid = '{' + str(uuid.uuid4()) + '}'

    def __cmp__(self, other):
        return cmp(self.name, other.name)

    def __eq__(self, other):
        return False if cmp(self.name, other.name) else True

    def __hash__(self):
        return hash(self.name)


class GroupMap(object):

    group_map = {
        '.c': 'ClCompile',
        '.cpp': 'ClCompile',
        '.h': 'ClInclude',
        '.hpp': 'ClInclude',
        '.xml': 'Xml',
    }

    @classmethod
    def get(self, key):
        return self.group_map.get(key, 'None')


class Group(object):
    
    def __init__(self, name):
        self.name = name

    def __cmp__(self, other):
        return cmp(self.name, other.name)

    def __eq__(self, other):
        return False if cmp(self.name, other.name) else True

    def __hash__(self):
        return hash(self.name)


class File(object):

    def __init__(self, path):
        """
            As to a path ai\sync_ai_def.h
            the project name is "sync"
            the filter is "ai"
            the group is 'ClInclude'
        """
        self.path = path
        self.abs_path = None	# init after added to a project
        self.filter_name = os.path.dirname(path)
        self.group_name = GroupMap.get(os.path.splitext(path)[-1])

    def __cmp__(self, other):
        return cmp(self.path, other.path)

    def __eq__(self, other):
        return False if cmp(self.path, other.path) else True

    def __hash__(self):
        return hash(self.path)


class VSProjectGenerator(object):
    
    def __init__(self, config):
        self.config = config

    def generate(self):
        solution = Solution(self.config.solution_name)
        default_project = Project(self.config.solution_name)

        if self.config.single_project:
            # 单工程解决方案
            for file_path in self.walk(self.config.src_path):
                if os.path.splitext(os.path.basename(file_path))[-1] in self.config.ext_exclude:
                    continue
                path = os.path.relpath(file_path, self.config.src_path)
                file_obj = File(path)
                default_project.add_file(file_obj, root_dir=True)
            solution.add_project(default_project)
        else:
            # 多工程解决方案
            for entry in scandir.scandir(self.config.src_path):
                if entry.is_dir():
                    if entry.name in self.config.dir_exclude:
                        continue
                    print 'Generating project', entry.name, '...' 
                    project = Project(entry.name)
                    for file_path in self.walk(entry.path):
                        if os.path.splitext(os.path.basename(file_path))[-1] in self.config.ext_exclude:
                            continue
                        path = os.path.relpath(file_path, os.path.join(self.config.src_path, entry.name))
                        file_obj = File(path)
                        project.add_file(file_obj)
                    solution.add_project(project)
                elif entry.is_file():
                    if os.path.splitext(entry.name)[-1] in self.config.ext_exclude:
                        continue
                    path = os.path.relpath(entry.path, self.config.src_path)
                    file_obj = File(path)
                    default_project.add_file(file_obj, root_dir=True)
            solution.add_project(default_project)

        tr = TemplateRender()
        solution.export(tr, self.config.output_path)

    #def walk(self):
    #    self._walk(self.src_path)

    def walk(self, dirname):
        file_list = []
        for entry in scandir.scandir(dirname):
            if entry.is_dir():
                file_list += self.walk(entry.path)
            elif entry.is_file():
                # print entry.name
                file_list.append(entry.path)
            else:
                continue
        return file_list
