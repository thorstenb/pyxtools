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
# Output to file support by Cedric Bosdonnat <cedricbosdo@openoffice.org>
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

    def __init__(self, fd):
        self._fd = fd

    def write (self, msg):
        if self._fd is not None:
            self._fd.write(msg+"\n")
        else:
            print msg

    def setDocumentLocator (self, locator):
        pass

    def encode (self,s):
        return s.replace("\\",r"\\").replace("\n",r"\n").replace("\t",r"\t")

    def startElementNS (self, name, qname, attrs):
        self.write("({%s}%s" % name)
        keys = attrs.keys()
        keys.sort()
        for n in keys:
            self.write("A{%s}%s %s" % (n[0], n[1], (self.encode(attrs[n]))))

    def endElementNS (self, name, qname):
        self.write("){%s}%s" % name)

    def characters (self, content):
        self.write("-%s" % self.encode(content))

    def processingInstruction (self, target, data):
        self.write("?%s %s" % (target, self.encode(data)))

if __name__ == "__main__":
    import sys
    import codecs
    
    parser = xml.sax.make_parser()
    parser.setFeature(xml.sax.handler.feature_namespaces, True)
    parser.setFeature(xml.sax.handler.feature_namespace_prefixes, False)
    out = None
    if len(sys.argv) == 3 and sys.argv[2] != "-":
        out = codecs.open(sys.argv[2], encoding='utf-8', mode='w')
    parser.setContentHandler(PyxConverter( out ))
    parser.setEntityResolver(DummyResolver())

    parser.parse(open(sys.argv[1],"r"))
    if out is not None:
        out.close()
