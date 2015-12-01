#! /usr/bin/python3
# -*- coding-utf-8 -*-

"""
This script transform a md into a plain html in the context of a
documentation for Kit&Pack.
"""

from lib.geoReader import geoReader

print("---------------------------- geo --")
print("-- by antoine.delhomme@espci.org --")
print("-----------------------------------")

doc_in = "doc/001-v2-doc"
dir_out = "./doc"

# Read the document
with geoReader(doc_in, dir_out) as g:
    g.parse()
