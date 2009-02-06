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

import os
import string

import TestSCons

test = TestSCons.TestSCons()

no_such_file = test.workpath("no_such_file")

test.write("f1.in", "\n")

test.write('SConstruct', r"""
bld = Builder(action = '%s $SOURCES $TARGET')
env = Environment(BUILDERS = { 'bld' : bld })
env.bld(target = 'f1', source = 'f1.in')
""" % string.replace(no_such_file, '\\', '\\\\'))

test.run(arguments='.',
         stdout = test.wrap_stdout("%s f1.in f1\n" % no_such_file, error=1),
         stderr = None,
         status = 2)

bad_command = """\
Bad command or file name
"""

unrecognized = """\
'%s' is not recognized as an internal or external command,
operable program or batch file.
scons: *** [%s] Error 1
"""

unspecified = """\
The name specified is not recognized as an
internal or external command, operable program or batch file.
scons: *** [%s] Error 1
"""

not_found_1 = """
sh: %s: not found
scons: *** [%s] Error 1
"""

not_found_2 = """
sh: %s:  not found
scons: *** [%s] Error 1
"""

not_found_127 = """\
sh: %s: not found
scons: *** [%s] Error 127
"""

No_such = """\
%s: No such file or directory
scons: *** [%s] Error 127
"""

test.description_set("Incorrect STDERR:\n%s\n" % test.stderr())
if os.name == 'nt':
    errs = [
        bad_command,
        unrecognized % (no_such_file, 'f1'),
        unspecified % 'f1'
    ]
    test.fail_test(not test.stderr() in errs)
else:
    errs = [
        not_found_1 % (no_such_file, 'f1'),
        not_found_2 % (no_such_file, 'f1'),
        not_found_127 % (no_such_file, 'f1'),
        No_such % (no_such_file, 'f1'),
    ]
    test.must_contain_any_line(test.stderr(), errs)

test.pass_test()
