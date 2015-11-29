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

doc_in = "./001-v2-doc"

class geoReader():

    def __init__(self, doc_name):
        self.doc_name = doc_name
        self.doc_in = "%s.md" % self.doc_name
        self.doc_out = "%s.html" % self.doc_name

        self.header = None
        self.header_limit = -1

    def __enter__(self):
        """Open the file.
        """

        self.f_in = open(self.doc_in, 'r')
        self.f_out = open(self.doc_out, 'w')

        return self

    def __exit__(self, type, value, traceback):
        """Close the file.
        """
        self.f_in.close()
        self.f_out.close()

    def parseHeader(self):
        """Parse the header of the file.
        """
        s = mmap.mmap(self.f_in.fileno(), 0, access=mmap.ACCESS_READ)
        self.header_limit = s.find(b'---')

        if self.header_limit != -1:
            self.header = yaml.load(s[0:self.header_limit])
            print(self.header['name'])
        else:
            print("Cannot load the header")



# Read the document
with geoReader(doc_in) as g:
    g.parseHeader()
