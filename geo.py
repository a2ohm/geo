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
        self.doc_out = ""

        self.f_in = None
        self.f_in_mmap = None

        self.header = None
        self.header_limit = -1

    def __enter__(self):
        """Open the file.
        """

        self.f_in = open(self.doc_in, 'r')

        return self

    def __exit__(self, type, value, traceback):
        """Close the file.
        """
        self.f_in.close()

    def parseHeader(self):
        """Parse the header of the file.
        """

        if self.header_limit < 0:
            self.f_in_mmap = mmap.mmap(self.f_in.fileno(),
                    0, access=mmap.ACCESS_READ)
            self.header_limit = self.f_in_mmap.find(b'---')

            if self.header_limit != -1:
                self.header = yaml.load(
                        self.f_in_mmap[0:self.header_limit])
            else:
                raise("Cannot load the header")

    def parseLine(self, line):
        """Parse a line.
        """
        line_parsed = line
        return line_parsed

    def parse(self):
        """Parse all the document.
        """

        # Parse the header
        self.parseHeader()

        # Init the output file
        self.doc_out = "%s.html" % self.header['version']

        with open(self.doc_out, 'w') as f_out:
            # Parse the rest of the document
            self.f_in.seek(self.header_limit)

            for line in self.f_in.readlines():
                # Parse the line
                line_parsed = self.parseLine(line)

                # Write it out
                f_out.write(line_parsed)




# Read the document
with geoReader(doc_in) as g:
    g.parse()
