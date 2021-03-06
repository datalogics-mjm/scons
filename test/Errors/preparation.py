#!/usr/bin/env python
#
# __COPYRIGHT__
#
# Permission is hereby granted, free of charge, to any person obtaining
# a copy of this software and associated documentation files (the
# "Software"), to deal in the Software without restriction, including
# without limitation the rights to use, copy, modify, merge, publish,
# distribute, sublicense, and/or sell copies of the Software, and to
# permit persons to whom the Software is furnished to do so, subject to
# the following conditions:
#
# The above copyright notice and this permission notice shall be included
# in all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY
# KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE
# WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND
# NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE
# LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION
# OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION
# WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
#

__revision__ = "__FILE__ __REVISION__ __DATE__ __DEVELOPER__"

"""
Verify that we print a useful message (and exit non-zero) if an external
error occurs while deciding if a Node is current or not.
"""

import sys

import TestSCons

test = TestSCons.TestSCons()

install = test.workpath('install')
install_file = test.workpath('install', 'file')
work_file = test.workpath('work', 'file')

test.subdir('install', 'work')

test.write(['work', 'SConstruct'], """\
Alias("install", Install(r"%(install)s", File('file')))

# Make a directory where we expect the File() to be.  This causes an
# IOError or OSError when we try to open it to read its signature.
import os
os.mkdir(r'%(work_file)s')
""" % locals())

if sys.platform == 'win32':
    error_message = "Permission denied"
else:
    error_message = "Is a directory"

expect = """\
scons: *** [%(install_file)s] %(work_file)s: %(error_message)s
""" % locals()

test.run(chdir = 'work',
         arguments = 'install',
         status = 2,
         stderr = expect)

test.pass_test()
