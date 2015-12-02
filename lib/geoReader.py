#! /usr/bin/python
# -*- coding-utf-8 -*-

import mmap
import yaml
import re

class geoReader():

    def __init__(self, doc_in, dir_out = "./doc"):
        self.doc_in = doc_in

        self.doc_out = ""
        self.dir_out = dir_out

        self.f_in = None

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
            f_in_mmap = mmap.mmap(self.f_in.fileno(),
                    0, access=mmap.ACCESS_READ)
            self.header_limit = f_in_mmap.find(b'---')

            if self.header_limit != -1:
                self.header = yaml.load(
                        f_in_mmap[0:self.header_limit])
            else:
                raise("Cannot load the header")

    def parseLine(self, line):
        """Parse a line.
        """

        # Regex
        re_title = re.match("(#+) (.+)", line)
        re_img = re.match("\!\[(.+)\]\((.+)\)", line)

        rejected = ["---\n"]

        # Init the parsed line
        line_parsed = ""

        if line in rejected:
            line_parsed += ""

        elif re_title:
            line_parsed += self.parse_title(re_title)

        elif re_img:
            line_parsed += self.parse_image(re_img)

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
        self.doc_out = "%s/%s.php" % (
                self.dir_out, self.header['version'])

        with open(self.doc_out, 'w') as f_out:
            # Write down the header
            # ... version
            f_out.write(
                    "<p>Documentation %s</p>\n"
                    % self.header["version"])

            # ... parts list
            f_out.write("\n")
            f_out.write(
                "<section id=\"partsList\">\n" \
                "<h2>Composants</h2>\n" \
                "<dl>\n")

            for item in self.header["items"]:
                img = self.write_img(src=item['img'],
                        alt=item['description'])

                f_out.write(
                        "   <dt>%s</dt>\n" \
                        "   <dd>%s</dd>\n" % (
                        img, item["description"]))

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

    # ----------------
    # -- subparsers --
    # ----------------

    def parse_title(self, re_title):
        """Parse a title based on the resuslt of the regex.
        """
        rank = len(re_title.group(1)) + 2
        title = re_title.group(2)

        return "\n<h%d>%s</h%d>\n" % (
                rank, title, rank)

    def parse_image(self, re_img):
        """Parse an image based on the resuslt of the regex.
        """
        src = re_img.group(1)
        alt = re_img.group(2)

        parsed_line  = "\n"
        parsed_line += self.write_img(src, alt)
        parsed_line += "\n"

        return parsed_line

    # -------------
    # -- writers --
    # -------------

    def write_img(self, src, alt="", autoPath = True):
        if autoPath == True:
            src = "../i/doc/%s/%s" % (self.header['long_project_id'], src)
        return "<img src=\"%s\" alt=\"%s\" />" % (src, alt)
