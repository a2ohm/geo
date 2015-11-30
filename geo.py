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

doc_in = "./doc/001-v2-doc"

class geoReader():

    def __init__(self, doc_name):
        self.doc_name = doc_name
        self.doc_in = "%s.md" % self.doc_name
        self.doc_out = ""

        self.f_in = None
        self.f_in_mmap = None

        self.header = None
        self.header_limit = -1

        # Parsing flags
        self.pf_inP = False

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

        rejected = ["---\n"]

        line_parsed = ""

        if line in rejected:
            line_parsed += ""

        elif line[0] == "#":
            line_parsed += "\n<h3>%s</h3>\n" % line[2:-1]

        elif line == "\n":
            if self.pf_inP:
                # Close a paragrah
                self.pf_inP = False
                line_parsed += "</p>\n"
            else:
                line_parsed += ""

        else:
            if not self.pf_inP:
                self.pf_inP = True
                line_parsed += "\n<p>"

            line_parsed += "%s " % line[:-1]

        return line_parsed

    def parse(self):
        """Parse all the document.
        """
        
        # Reset flags
        self.pf_inP = False

        # Parse the header
        self.parseHeader()

        # Init the output file
        self.doc_out = "%s.php" % self.header['version']

        with open(self.doc_out, 'w') as f_out:
            # Write down the header
            # ... version
            f_out.write(
                    "<p>Documentation %s</p>\n"
                    % self.header["version"])

            # ... parts list
            f_out.write("\n")
            f_out.write(
                "<section id=r\"partsList\">\n" \
                "<h2>Composants</h2>\n" \
                "<dl>\n")

            for item in self.header["items"]:
                src = "../i/doc/%s/%s" % (
                    self.header["version"],
                    item["img"])

                f_out.write(
                        "   <dt><img src=\"%s\" /></dt>\n" \
                        "   <dd>%s</dd>\n" % (
                        src, item["description"]))

            f_out.write(
                    "</dl>\n" \
                    "\n" \
                    "</section>\n")

            # ... intro
            f_out.write("\n")
            f_out.write(
                    "<section id=\"doc\">\n" \
                    "<h2>Notice de montage</h2>\n")

            # Parse the rest of the document
            self.f_in.seek(self.header_limit)

            for line in self.f_in.readlines():
                # Parse the line
                line_parsed = self.parseLine(line)

                # Write it out
                f_out.write(line_parsed)

            # Close any open paragraph
            if self.pf_inP:
                self.pg_inP = False
                f_out.write("</p>\n")

            # ... ending
            f_out.write("\n")
            f_out.write("</section>")


# Read the document
with geoReader(doc_in) as g:
    g.parse()
