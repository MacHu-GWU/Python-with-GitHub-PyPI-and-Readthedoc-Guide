from __future__ import print_function
from docfly import Docfly
import os

try:
    os.remove(r"source\canbeAny")
except Exception as e:
    print(e)
     
docfly = Docfly("canbeAny", dst="source")
docfly.fly()