#! /usr/bin/python
# -*- coding-utf-8 -*-

import mmap
import yaml
import re

class geoBuilder():

    def __init__(self, project_id, versions, dir_out = "./doc"):
        self.project_id = project_id
        self.versions = versions

        self.dir_out = dir_out

    def makeDocFile(self):
        """Generate the main doc file.
        """

        f_out = "%s/%s-doc.php" %  (self.dir_out, self.project_id)
        version = max(self.versions)

        with open(f_out, 'w') as f:
            f.write("<!DOCTYPE html>\n" \
                    "<html xmlns=\"http://www.w3.org/1999/xhtml\">\n" \
                    "<head>\n" \
                    "<meta http-equiv=\"Content-Type\" content=\"text/html; charset=utf-8\"/>\n" \
                    "\n" \
                    "<title>Kit&Pack − Ultimate Power Booster</title>\n" \
                    "<link rel=\"shortcut icon\" type=\"image/png\" href=\"../favicon.png\"/>" \
                    "<link rel=\"stylesheet\" type=\"text/css\" href=\"../css/doc-1.css\" />\n"
                    "\n" \
                    "</head>\n" \
                    "<body>\n" \
                    "\n" \
                    "<h1>Ultimate Power Booster</h1>" \
                    "\n")

            # Write a list of other versions of the documentation
            f.write("<p>Versions de cette documentation.</p>\n")
            f.write("<ul>\n")
            for v in self.versions:
                f.write("\t<li><a href=\"%s.php\" />%s</a></li>\n" % (
                    v, v))
            f.write("</ul>\n\n")

            f.write("<?php\n" \
                    "include(\"%s.php\")\n" \
                    "?>\n" \
                    "\n" \
                    "</body>\n" \
                    "</html>" % (version))
            
