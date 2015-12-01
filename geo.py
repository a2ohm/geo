#! /usr/bin/python3
# -*- coding-utf-8 -*-

"""
This script transform a md into a plain html in the context of a
documentation for Kit&Pack.
"""

import argparse
from lib.geoReader import geoReader

print("---------------------------- geo --")
print("-- by antoine.delhomme@espci.org --")
print("-----------------------------------")

# Parse arguments
parser = argparse.ArgumentParser(
    description='Build the web version of Kit&Pack documentation.')

parser.add_argument('-i', dest='doc_in', required=True,
    help='Input file')
parser.add_argument('-o', dest='dir_out', required=True,
    help='Output directory')

args = parser.parse_args()

doc_in = args.doc_in
dir_out = args.dir_out

# Read the document
with geoReader(doc_in, dir_out) as g:
    g.parse()
