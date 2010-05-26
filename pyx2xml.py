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
# Inspired by Sean McGrath's pyx2xml, and David Mertz' XML matters
# Cobbled together by Thorsten Behrens <thb@openoffice.org>
#
import sys, os, re

def grabNS (qname):
   global num_ns, uris
   delimit = qname.find('}')
   uri = qname[1:delimit]
   name = qname[delimit+1:]
   if not uri in uris:
      num_ns += 1
      uris[uri] = 'ns'+str(num_ns)
   return uris[uri] + ':' + name   

num_ns = 0
get_attrs = 0
uris = {}
lines = []

unescape = lambda s: s.replace(r'\t','\t').replace(r'\n','\n').replace(r'\\','\\')
ns_handling = len(sys.argv) > 1 and sys.argv[1] == '-ns'
if ns_handling:
   writeln = lambda s: lines.append(s)
else:
   writeln = lambda s: sys.stdout.write(s+'\n')

writeln('<?xml version="1.0" encoding="UTF-8"?>')
curr_line=""
for line in sys.stdin:
   if get_attrs and line[0] != 'A':
      # attr section ends here
      get_attrs = 0
      curr_line += '>'
   if line[0] == '?':
      writeln(curr_line+'<?%s?>' % line[1:-1])
      curr_line=""
   elif line[0] == '(':
      curr_line += '<%s' % grabNS(line[1:-1])
      get_attrs = 1
   elif line[0] == 'A':
      name,val = line[1:].split(None, 1)
      curr_line += ' %s="%s"' % (grabNS(name), unescape(val)[:-1])
   elif line[:3] == r'-\n':
      writeln(curr_line)
      curr_line=""
   elif line[0] == '-':
      curr_line += unescape(line[1:-1])
   elif line[0] == ')':
      curr_line += '</%s>' % grabNS(line[1:-1])

if len(curr_line):
   writeln(curr_line)

if ns_handling:
   opening_tag=re.compile("(\\s*<\\s*)([^\\? \\t\\n\\r\\f\\v]+)")
   ns_written=False
   for line in lines:
      if not ns_written and re.match(opening_tag,line):
         line = re.split(opening_tag,line)
         line.insert(3, ' ' + ' '.join(['xmlns:'+n+'="'+u+'"' for (u,n) in uris.items()]))
         sys.stdout.write(''.join(line) + '\n')
         ns_written = True
      else:
         sys.stdout.write(line+'\n')
