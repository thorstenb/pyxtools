#!/usr/bin/env python
#
# Licensed under the Apache License, Version 2.0 (the "License"); you may
# not use this file except in compliance with the License. You may obtain a
# copy of the License at:
#
#            http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
# WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
# License for the specific language governing permissions and limitations
# under the License.
#
# Inspired by Sean McGrath's html2pyx, and Peter A. Bigot's saxutils
# Cobbled together by Thorsten Behrens <thb@openoffice.org>
#
import xml.sax
import string
import StringIO

class DummyResolver:
    """Dummy - ignore PIs we dont' care about."""
    def resolveEntity (self, p, s):
        return StringIO.StringIO('')

class PyxConverter (xml.sax.handler.ContentHandler):
    """SAX handler class that transforms xml into pyx."""

    def setDocumentLocator (self, locator):
        pass

    def encode (self,s):
        return s.replace("\\",r"\\").replace("\n",r"\n").replace("\t",r"\t")
        return s

    def startElementNS (self, name, qname, attrs):
        print "({%s}%s" % name
        for (n,v) in attrs.items():
            print "A{%s}%s %s" % (n[0], n[1], (self.encode(v)))

    def endElementNS (self, name, qname):
        print "){%s}%s" % name

    def characters (self, content):
        print "-%s" % self.encode(content)

    def processingInstruction (self, target, data):
        print "?%s %s" % (target, self.encode(data))

if __name__ == "__main__":
    import sys
    
    parser = xml.sax.make_parser()
    parser.setFeature(xml.sax.handler.feature_namespaces, True)
    parser.setFeature(xml.sax.handler.feature_namespace_prefixes, False)
    parser.setContentHandler(PyxConverter())
    parser.setEntityResolver(DummyResolver())

    parser.parse(open(sys.argv[1],"r"))
