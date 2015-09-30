#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import print_function
from docfly import Docfly
import shutil
 
try:
    shutil.rmtree(r"source\canbeAny")
except Exception as e:
    print(e)
     
docfly = Docfly("canbeAny", dst="source")
docfly.fly()
