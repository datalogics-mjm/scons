#!/usr/bin/env python
#
# Copyright (c) 2001 Steven Knight
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
import TestCmd
import TestSCons

test = TestSCons.TestSCons()

no_such_file = test.workpath("no_such_file")
not_executable = test.workpath("not_executable")

test.write(not_executable, "\n")

test.write("f1.in", "\n")
test.write("f2.in", "\n")
test.write("f3.in", "\n")

test.write('SConstruct1', r"""
bld = Builder(name = 'bld', action = '%s $SOURCES $TARGET')
env = Environment(BUILDERS = [bld])
env.bld(target = 'f1', source = 'f1.in')
""" % string.replace(no_such_file, '\\', '\\\\'))

test.run(arguments='-f SConstruct1 .',
	 stdout = "%s f1.in f1\n" % no_such_file,
         stderr = None)

bad_command = "Bad command or file name\n"

unrecognized = """'%s' is not recognized as an internal or external command,
operable program or batch file.
scons: *** [%s] Error 1
"""

unspecified = """The name specified is not recognized as an
internal or external command, operable program or batch file.
scons: *** [%s] Error 1
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
    test.fail_test(test.stderr() != """sh: %s: No such file or directory
scons: *** [f1] Error 127
""" % no_such_file)


test.write('SConstruct2', r"""
bld = Builder(name = 'bld', action = '%s $SOURCES $TARGET')
env = Environment(BUILDERS = [bld])
env.bld(target = 'f2', source = 'f2.in')
""" % string.replace(not_executable, '\\', '\\\\'))

test.run(arguments='-f SConstruct2 .',
	 stdout = "%s f2.in f2\n" % not_executable,
	 stderr = None)

test.description_set("Incorrect STDERR:\n%s\n" % test.stderr())
if os.name == 'nt':
    errs = [
        bad_command,
        unrecognized % (no_such_file, 'f2'),
        unspecified % 'f2'
    ]
    test.fail_test(not test.stderr() in errs)
else:
    test.fail_test(test.stderr() != """sh: %s: Permission denied
scons: *** [f2] Error 126
""" % not_executable)

test.write('SConstruct3', r"""
bld = Builder(name = 'bld', action = '%s $SOURCES $TARGET')
env = Environment(BUILDERS = [bld])
env.bld(target = 'f3', source = 'f3.in')
""" % string.replace(test.workdir, '\\', '\\\\'))

test.run(arguments='-f SConstruct3 .',
	 stdout = "%s f3.in f3\n" % test.workdir,
	 stderr = None)

test.description_set("Incorrect STDERR:\n%s\n" % test.stderr())
if os.name == 'nt':
    errs = [
        bad_command,
        unrecognized % (no_such_file, 'f3'),
        unspecified % 'f3'
    ]
    test.fail_test(not test.stderr() in errs)
else:
    test.fail_test(test.stderr() != """sh: %s: is a directory
scons: *** [f3] Error 126
""" % test.workdir)

test.pass_test()
