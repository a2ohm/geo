#! /usr/bin/python3
# -*- coding-utf-8 -*-

"""
This script transform a md into a plain html in the context of a
documentation for Kit&Pack.
"""

import argparse
import os
import re
from os.path import join, getsize

from lib.geoReader import geoReader

print("------------------------- geoAll --")
print("-- by antoine.delhomme@espci.org --")
print("-----------------------------------")

# Parse arguments
parser = argparse.ArgumentParser(
    description='Build the web version of Kit&Pack documentation.')

parser.add_argument('-i', dest='dir_in', required=True,
    help='Input directory')
parser.add_argument('-o', dest='dir_out', required=True,
    help='Output directory')

args = parser.parse_args()

dir_in = args.dir_in
dir_out = args.dir_out

versions = {}

for root, dirs, files in os.walk(dir_in):
    if '.git' in dirs:
        # Do not explore the .git dir
        dirs.remove('.git')

    if dir_in == root:
        # Skip the root directory
        continue

    # Filter files to keep *.md files
    filesToProcess = [ root + "/" + f for f in files if re.match('.+\.md', f) ]

    # Process each of them
    for f in filesToProcess:

        with geoReader(f, dir_out) as g:
            # Parse the file
            g.parse()

            # List version of docs by project
            project_id = g.header['long_project_id']
            version = versions.get(project_id, [])
            versions[project_id] = version + [g.header['version']]

print(versions)
