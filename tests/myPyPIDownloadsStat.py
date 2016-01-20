#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
vanity is a command line tools to get PyPI download stats information.
"""

from __future__ import print_function

from vanity import downloads_total

if __name__ == "__main__":
    SanhesPyPIPorjects = [
        "windtalker",
        "ctmatching",
        "sqlite4dummy",
        "typarse",
        "uszipcode",
        "geomate",
        "pyknackhq",
        "docfly",
        "angora", 
    ]
    
    total = 0
    hist = list()
    for project in SanhesPyPIPorjects:
        downloads = downloads_total(project, verbose=False)
        hist.append((project, downloads))
        total += downloads
    hist = sorted(hist, key=lambda x: x[1], reverse=True)
    
    for project, downloads in hist:
        print("%r total downloads %s" % (project, downloads))
    print("Sanhe's open source project total downloads %s" % total)