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
Verify that the File() global function and environment method work
correctly, and that the former does not try to expand construction
variables.
"""

import TestSCons

test = TestSCons.TestSCons()

test.write('SConstruct', """
env = Environment(FOO = 'fff', BAR = 'bbb')
print File('ddd')
print File('$FOO')
print File('${BAR}_$BAR')
print env.File('eee')
print env.File('$FOO')
print env.File('${BAR}_$BAR')
""")

test.run(stdout = test.wrap_stdout(read_str = """\
ddd
$FOO
${BAR}_$BAR
eee
fff
bbb_bbb
""", build_str = """\
scons: `.' is up to date.
"""))

test.pass_test()
