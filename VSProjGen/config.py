# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import os
import json


class Config(object):
    
    CONFIG_FILE = 'config.json'

    def __init__(self):
        self._config = None
        self.load()

    def load(self):
        with open(self.CONFIG_FILE, 'r') as f:
            self._config = json.load(f)

    def __getitem__(self, key):
        return self._config[key]
    