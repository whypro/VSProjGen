# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import os
import uuid
from collections import defaultdict

from jinja2 import Environment, Template, FileSystemLoader
import scandir

from .config import Config


config = Config()


project_type_guid_map = {
    'ASP.NET MVC 1.0': '{603C0E0B-DB56-11DC-BE95-000D561079B0}', 
    'ASP.NET MVC 2.0': '{F85E285D-A4E0-4152-9332-AB1D724D3325}', 
    'ASP.NET MVC 3.0': '{E53F8FEA-EAE0-44A6-8774-FFD645390401}',
    'ASP.NET MVC 4.0': '{E3E379DF-F4C6-4180-9B81-6769533ABE47}',
    'C#': '{FAE04EC0-301F-11D3-BF4B-00C04F79EFBC}',
    'C++': '{8BC9CEB8-8B4A-11D0-8D11-00A0C91BC942}',
    'Database': '{A9ACE9BB-CECE-4E62-9AA4-C7E7C5BD2124}',
    'Database (other project types)': '{4F174C21-8C12-11D0-8340-0000F80270F8}',
    'Deployment Cab': '{3EA9E505-35AC-4774-B492-AD1749C4943A}',
    'Deployment Merge Module': '{06A35CCD-C46D-44D5-987B-CF40FF872267}',
    'Deployment Setup': '{978C614F-708E-4E1A-B201-565925725DBA}',
    'Deployment Smart Device Cab': '{AB322303-2255-48EF-A496-5904EB18DA55}',
    'Distributed System': '{F135691A-BF7E-435D-8960-F99683D2D49C}',
    'F#': '{F2A71F9B-5D33-465A-A702-920D77279786}',
    'J#': '{E6FDF86B-F3D1-11D4-8576-0002A516ECE8}',
    'Legacy (2003) Smart Device (C#)': '{20D4826A-C6FA-45DB-90F4-C717570B9F32}',
    'Legacy (2003) Smart Device (VB.NET)': '{CB4CE8C6-1BDB-4DC7-A4D3-65A1999772F8}',
    'Model-View-Controller v2 (MVC2)': '{F85E285D-A4E0-4152-9332-AB1D724D3325}',
    'Model-View-Controller v3 (MVC3)': '{E53F8FEA-EAE0-44A6-8774-FFD645390401}',
    'Model-View-Controller v4 (MVC4)': '{E3E379DF-F4C6-4180-9B81-6769533ABE47}',
    'Mono for Android': '{EFBA0AD7-5A72-4C68-AF49-83D382785DCF}',
    'MonoTouch': '{6BC8ED88-2882-458C-8E55-DFD12B67127B}',
    'MonoTouch Binding': '{F5B4F3BC-B597-4E2B-B552-EF5D8A32436F}',
    'Portable Class Library': '{786C830F-07A1-408B-BD7F-6EE04809D6DB}',
    'SharePoint (C#)': '{593B0543-81F6-4436-BA1E-4747859CAAE2}',
    'SharePoint (VB.NET)': '{EC05E597-79D4-47f3-ADA0-324C4F7C7484}',
    'SharePoint Workflow': '{F8810EC1-6754-47FC-A15F-DFABD2E3FA90}',
    'Silverlight': '{A1591282-1198-4647-A2B1-27E5FF5F6F3B}',
    'Smart Device (C#)': '{4D628B5B-2FBC-4AA6-8C16-197242AEB884}',
    'Smart Device (VB.NET)': '{68B1623D-7FB9-47D8-8664-7ECEA3297D4F}',
    'Test': '{3AC096D0-A1C2-E12C-1390-A8335801FDAB}',
    'VB.NET': '{F184B08F-C81C-45F6-A57F-5ABD9991F28F}',
    'Visual Database Tools': '{C252FEB5-A946-4202-B1D4-9916A0590387}',
    'Visual Studio Tools for Applications (VSTA)': '{A860303F-1F3F-4691-B57E-529FC101A107}',
    'Visual Studio Tools for Office (VSTO)': '{BAA0C2D2-18E2-41B9-852F-F413020CAA33}',
    'Web Application': '{349C5851-65DF-11DA-9384-00065B846F21}',
    'Web Site': '{E24C65DC-7377-472B-9ABA-BC803B73C61A}',
    'Windows (C#)': '{FAE04EC0-301F-11D3-BF4B-00C04F79EFBC}',
    'Windows (VB.NET)': '{F184B08F-C81C-45F6-A57F-5ABD9991F28F}',
    'Windows (Visual C++)': '{8BC9CEB8-8B4A-11D0-8D11-00A0C91BC942}',
    'Windows Communication Foundation (WCF)': '{3D9AD99F-2412-4246-B90B-4EAA41C64699}',
    'Windows Presentation Foundation (WPF)': '{60DC8134-EBA5-43B8-BCC9-BB4BC16C2548}',
    'Windows Store Apps (Metro Apps)': '{BC8A1FFA-BEE3-4634-8014-F334798102B3}',
    'Workflow (C#)': '{14822709-B5A1-4724-98CA-57A101D1B079}',
    'Workflow (VB.NET)': '{D59BE175-2ED0-4C54-BE3D-CDAA9F3214C8}',
    'Workflow Foundation': '{32F31D43-81CC-4C15-9DE6-3FC5453562B6}',
    'Xamarin.Android': '{EFBA0AD7-5A72-4C68-AF49-83D382785DCF}',
    'Xamarin.iOS': '{6BC8ED88-2882-458C-8E55-DFD12B67127B}',
    'XNA (Windows)': '{6D335F3A-9D43-41b4-9D22-F6F17C4BE596}',
    'XNA (XBox)': '{2DF5C3F4-5A5F-47a9-8E94-23B4456F55E2}',
    'XNA (Zune)': '{D399B71A-8929-442a-A9AC-8BEC78BB2433}',
}


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
