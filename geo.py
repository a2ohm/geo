#! /usr/bin/python3
# -*- coding-utf-8 -*-

"""
This script transform a md into a plain html in the context of a
documentation for Kit&Pack.
"""

import mmap
import yaml

print("---------------------------- geo --")
print("-- by antoine.delhomme@espci.org --")
print("-----------------------------------")

doc_in = "./001-v2-doc.md"

class geoReader():

    def __init__(self, doc_in):
        self.doc_in = doc_in
        self.header = None

    def __enter__(self):
        """Open the file.
        """
        self.f = open(self.doc_in, 'r')

        return self

    def __exit__(self, type, value, traceback):
        """Close the file.
        """
        self.f.close()

    def parseHeader(self):
        """Parse the header of the file.
        """
        s = mmap.mmap(self.f.fileno(), 0, access=mmap.ACCESS_READ)
        self.header_limit = s.find(b'---')

        if self.header_limit != -1:
            self.header = yaml.load(s[0:self.header_limit])
            print(self.header['name'])
        else:
            print("Cannot load the header")



# Read the document
with geoReader(doc_in) as g:
    g.parseHeader()
