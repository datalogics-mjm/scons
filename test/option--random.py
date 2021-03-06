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
Verify that we build correctly using the --random option.
"""

import os.path

import TestSCons

test = TestSCons.TestSCons()

test.write('SConstruct', """
def cat(env, source, target):
    target = str(target[0])
    source = map(str, source)
    f = open(target, "wb")
    for src in source:
        f.write(open(src, "rb").read())
    f.close()
env = Environment(BUILDERS={'Cat':Builder(action=cat)})
env.Cat('aaa.out', 'aaa.in')
env.Cat('bbb.out', 'bbb.in')
env.Cat('ccc.out', 'ccc.in')
env.Cat('all', ['aaa.out', 'bbb.out', 'ccc.out'])
""")

test.write('aaa.in', "aaa.in\n")
test.write('bbb.in', "bbb.in\n")
test.write('ccc.in', "ccc.in\n")

test.run(arguments = '--random .')

test.fail_test(test.read('all') != "aaa.in\nbbb.in\nccc.in\n")

test.run(arguments = '-q --random .')

test.run(arguments = '-c --random .')

test.fail_test(os.path.exists(test.workpath('aaa.out')))
test.fail_test(os.path.exists(test.workpath('bbb.out')))
test.fail_test(os.path.exists(test.workpath('ccc.out')))
test.fail_test(os.path.exists(test.workpath('all')))

test.run(arguments = '-q --random .', status = 1)

test.run(arguments = '--random .')

test.fail_test(test.read('all') != "aaa.in\nbbb.in\nccc.in\n")

test.pass_test()
