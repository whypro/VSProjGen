# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import time

from VSProjGen import VSProjectGenerator


__author__  = 'haoyuwang'
__date__ = '2016-09-29'


if __name__ == '__main__':

    begin = time.time()
    vspg = VSProjectGenerator()
    vspg.generate()
    print time.time() - begin

