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
Verify that config files specified with the -f and --file options
affect how the func subcommand processes things.
"""

import TestSCons_time

test = TestSCons_time.TestSCons_time(match = TestSCons_time.match_re)

try:
    import pstats
except ImportError:
    test.skip_test('No pstats module, skipping test.\n')

test.profile_data('foo-001-0.prof', 'prof1.py', '_main', """\
def _main():
    pass
""")

test.profile_data('foo-002-0.prof', 'prof2.py', '_main', """\
# line 1 (intentional comment to adjust starting line numbers)
def _main():
    pass
""")


test.write('st1.conf', """\
prefix = 'foo-001'
""")

expect1 = r'\d.\d\d\d prof1\.py:1\(_main\)' + '\n'

test.run(arguments = 'func -f st1.conf', stdout = expect1)


test.write('st2.conf', """\
prefix = 'foo'
title = 'ST2.CONF TITLE'
""")

expect2 = \
r"""set title "ST2.CONF TITLE"
set key bottom left
plot '-' title "Startup" with lines lt 1
# Startup
1 0.000
2 0.000
e
"""

test.run(arguments = 'func --file st2.conf --fmt gnuplot', stdout = expect2)


test.pass_test()
