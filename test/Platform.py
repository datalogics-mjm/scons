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

import TestSCons

test = TestSCons.TestSCons()

test.write('SConstruct', """
env = Environment()
Platform('cygwin')(env)
print "'%s'" % env['PROGSUFFIX']
assert env['SHELL'] == 'sh'
Platform('os2')(env)
print "'%s'" % env['PROGSUFFIX']
Platform('posix')(env)
print "'%s'" % env['PROGSUFFIX']
Platform('win32')(env)
print "'%s'" % env['PROGSUFFIX']
SConscript('SConscript')
""")

test.write('SConscript', """
env = Environment()
Platform('cygwin')(env)
print "'%s'" % env['LIBSUFFIX']
Platform('os2')(env)
print "'%s'" % env['LIBSUFFIX']
Platform('posix')(env)
print "'%s'" % env['LIBSUFFIX']
Platform('win32')(env)
print "'%s'" % env['LIBSUFFIX']
""")

expect = test.wrap_stdout(read_str = """'.exe'
'.exe'
''
'.exe'
'.a'
'.lib'
'.a'
'.lib'
""", build_str = 'scons: "." is up to date.\n')

test.run(arguments = ".", stdout = expect)

test.pass_test()

