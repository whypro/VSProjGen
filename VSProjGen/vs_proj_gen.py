# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import time

from VSProjGen import VSProjectGenerator


if __name__ == '__main__':

    begin = time.time()
    vspg = VSProjectGenerator(config)
    vspg.generate()
    print time.time() - begin

