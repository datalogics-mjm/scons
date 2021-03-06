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

import sys
import unittest

print sys.path
import cpp



basic_input = """
#include "file1-yes"
#include <file2-yes>
"""


substitution_input = """
#define FILE3   "file3-yes"
#define FILE4   <file4-yes>

#include FILE3
#include FILE4

#define XXX_FILE5       YYY_FILE5
#define YYY_FILE5       ZZZ_FILE5
#define ZZZ_FILE5       FILE5

#define FILE5   "file5-yes"
#define FILE6   <file6-yes>

#define XXX_FILE6       YYY_FILE6
#define YYY_FILE6       ZZZ_FILE6
#define ZZZ_FILE6       FILE6

#include XXX_FILE5
#include XXX_FILE6
"""


ifdef_input = """
#define DEFINED 0

#ifdef	DEFINED
#include "file7-yes"
#else
#include "file7-no"
#endif

#ifdef	NOT_DEFINED
#include <file8-no>
#else
#include <file8-yes>
#endif
"""


if_boolean_input = """
#define ZERO	0
#define ONE	1

#if ZERO
#include "file9-no"
#else
#include "file9-yes"
#endif

#if ONE
#include <file10-yes>
#else
#include <file10-no>
#endif

#if ZERO
#include "file11-no-1"
#elif ZERO
#include "file11-no-2"
#else
#include "file11-yes"
#endif

#if ZERO
#include <file12-no-1>
#elif ONE
#include <file12-yes>
#else
#include <file12-no-2>
#endif

#if ONE
#include "file13-yes"
#elif ZERO
#include "file13-no-1"
#else
#include "file13-no-2"
#endif

#if ONE
#include <file14-yes>
#elif ONE
#include <file14-no-1>
#else
#include <file14-no-2>
#endif
"""


if_defined_input = """
#define DEFINED 0

#if	defined(DEFINED)
#include "file15-yes"
#endif

#if	! defined(DEFINED)
#include <file16-no>
#else
#include <file16-yes>
#endif

#if	defined DEFINED
#include "file17-yes"
#endif

#if	! defined DEFINED
#include <file18-no>
#else
#include <file18-yes>
#endif
"""


expression_input = """
#define ZERO	0
#define ONE	1

#if	ZERO && ZERO
#include "file19-no"
#else
#include "file19-yes"
#endif

#if	ZERO && ONE
#include <file20-no>
#else
#include <file20-yes>
#endif

#if	ONE && ZERO
#include "file21-no"
#else
#include "file21-yes"
#endif

#if	ONE && ONE
#include <file22-yes>
#else
#include <file22-no>
#endif

#if	ZERO || ZERO
#include "file23-no"
#else
#include "file23-yes"
#endif

#if	ZERO || ONE
#include <file24-yes>
#else
#include <file24-no>
#endif

#if	ONE || ZERO
#include "file25-yes"
#else
#include "file25-no"
#endif

#if	ONE || ONE
#include <file26-yes>
#else
#include <file26-no>
#endif

#if	ONE == ONE
#include "file27-yes"
#else
#include "file27-no"
#endif

#if	ONE != ONE
#include <file28-no>
#else
#include <file28-yes>
#endif

#if	! (ONE == ONE)
#include "file29-no"
#else
#include "file29-yes"
#endif

#if	! (ONE != ONE)
#include <file30-yes>
#else
#include <file30-no>
#endif
"""


undef_input = """
#define	UNDEFINE	0

#ifdef	UNDEFINE
#include "file31-yes"
#else
#include "file31-no"
#endif

#undef	UNDEFINE

#ifdef	UNDEFINE
#include <file32-no>
#else
#include <file32-yes>
#endif
"""


macro_function_input = """
#define ZERO	0
#define ONE	1

#define	FUNC33(x)	"file33-yes"
#define	FUNC34(x)	<file34-yes>

#include FUNC33(ZERO)
#include FUNC34(ZERO)

#define FILE35		"file35-yes"
#define FILE36		<file36-yes>

#define	FUNC35(x, y)	FILE35
#define	FUNC36(x, y)	FILE36

#include FUNC35(ZERO, ONE)
#include FUNC36(ZERO, ONE)

#define FILE37		"file37-yes"
#define FILE38		<file38-yes>

#define	FUNC37a(x, y)	FILE37
#define	FUNC38a(x, y)	FILE38

#define	FUNC37b(x, y)	FUNC37a(x, y)
#define	FUNC38b(x, y)	FUNC38a(x, y)

#define	FUNC37c(x, y)	FUNC37b(x, y)
#define	FUNC38c(x, y)	FUNC38b(x, y)

#include FUNC37c(ZERO, ONE)
#include FUNC38c(ZERO, ONE)

#define FILE39		"file39-yes"
#define FILE40		<file40-yes>

#define	FUNC39a(x0, y0)	FILE39
#define	FUNC40a(x0, y0)	FILE40

#define	FUNC39b(x1, y2)	FUNC39a(x1, y1)
#define	FUNC40b(x1, y2)	FUNC40a(x1, y1)

#define	FUNC39c(x2, y2)	FUNC39b(x2, y2)
#define	FUNC40c(x2, y2)	FUNC40b(x2, y2)

#include FUNC39c(ZERO, ONE)
#include FUNC40c(ZERO, ONE)
"""


token_pasting_input = """
#define PASTE_QUOTE(q, name)	q##name##-yes##q
#define PASTE_ANGLE(name)	<##name##-yes>

#define FUNC41	PASTE_QUOTE(", file41)
#define FUNC42	PASTE_ANGLE(file42)

#include FUNC41
#include FUNC42
"""



#    pp_class = PreProcessor
#    #pp_class = DumbPreProcessor

#    pp = pp_class(current = ".",
#                  cpppath = ['/usr/include'],
#                  print_all = 1)
#    #pp(open(sys.argv[1]).read())
#    pp(input)


class cppTestCase(unittest.TestCase):
    def setUp(self):
        self.cpp = self.cpp_class(current = ".",
                                  cpppath = ['/usr/include'])

    def test_basic(self):
        """Test basic #include scanning"""
        expect = self.basic_expect
        result = self.cpp(basic_input)
        assert expect == result, (expect, result)

    def test_substitution(self):
        """Test substitution of #include files using CPP variables"""
        expect = self.substitution_expect
        result = self.cpp(substitution_input)
        assert expect == result, (expect, result)

    def test_ifdef(self):
        """Test basic #ifdef processing"""
        expect = self.ifdef_expect
        result = self.cpp(ifdef_input)
        assert expect == result, (expect, result)

    def test_if_boolean(self):
        """Test #if with Boolean values"""
        expect = self.if_boolean_expect
        result = self.cpp(if_boolean_input)
        assert expect == result, (expect, result)

    def test_if_defined(self):
        """Test #if defined() idioms"""
        expect = self.if_defined_expect
        result = self.cpp(if_defined_input)
        assert expect == result, (expect, result)

    def test_expression(self):
        """Test #if with arithmetic expressions"""
        expect = self.expression_expect
        result = self.cpp(expression_input)
        assert expect == result, (expect, result)

    def test_undef(self):
        """Test #undef handling"""
        expect = self.undef_expect
        result = self.cpp(undef_input)
        assert expect == result, (expect, result)

    def test_macro_function(self):
        """Test using macro functions to express file names"""
        expect = self.macro_function_expect
        result = self.cpp(macro_function_input)
        assert expect == result, (expect, result)

    def test_token_pasting(self):
        """Test taken-pasting to construct file names"""
        expect = self.token_pasting_expect
        result = self.cpp(token_pasting_input)
        assert expect == result, (expect, result)

class cppAllTestCase(cppTestCase):
    def setUp(self):
        self.cpp = self.cpp_class(current = ".",
                                  cpppath = ['/usr/include'],
                                  all=1)

class PreProcessorTestCase(cppAllTestCase):
    cpp_class = cpp.PreProcessor

    basic_expect = [
        ('include', '"', 'file1-yes'),
        ('include', '<', 'file2-yes'),
    ]

    substitution_expect = [
        ('include', '"', 'file3-yes'),
        ('include', '<', 'file4-yes'),
        ('include', '"', 'file5-yes'),
        ('include', '<', 'file6-yes'),
    ]

    ifdef_expect = [
        ('include', '"', 'file7-yes'),
        ('include', '<', 'file8-yes'),
    ]

    if_boolean_expect = [
        ('include', '"', 'file9-yes'),
        ('include', '<', 'file10-yes'),
        ('include', '"', 'file11-yes'),
        ('include', '<', 'file12-yes'),
        ('include', '"', 'file13-yes'),
        ('include', '<', 'file14-yes'),
    ]

    if_defined_expect = [
        ('include', '"', 'file15-yes'),
        ('include', '<', 'file16-yes'),
        ('include', '"', 'file17-yes'),
        ('include', '<', 'file18-yes'),
    ]

    expression_expect = [
        ('include', '"', 'file19-yes'),
        ('include', '<', 'file20-yes'),
        ('include', '"', 'file21-yes'),
        ('include', '<', 'file22-yes'),
        ('include', '"', 'file23-yes'),
        ('include', '<', 'file24-yes'),
        ('include', '"', 'file25-yes'),
        ('include', '<', 'file26-yes'),
        ('include', '"', 'file27-yes'),
        ('include', '<', 'file28-yes'),
        ('include', '"', 'file29-yes'),
        ('include', '<', 'file30-yes'),
    ]

    undef_expect = [
        ('include', '"', 'file31-yes'),
        ('include', '<', 'file32-yes'),
    ]

    macro_function_expect = [
        ('include', '"', 'file33-yes'),
        ('include', '<', 'file34-yes'),
        ('include', '"', 'file35-yes'),
        ('include', '<', 'file36-yes'),
        ('include', '"', 'file37-yes'),
        ('include', '<', 'file38-yes'),
        ('include', '"', 'file39-yes'),
        ('include', '<', 'file40-yes'),
    ]

    token_pasting_expect = [
        ('include', '"', 'file41-yes'),
        ('include', '<', 'file42-yes'),
    ]

class DumbPreProcessorTestCase(cppAllTestCase):
    cpp_class = cpp.DumbPreProcessor

    basic_expect = [
        ('include', '"', 'file1-yes'),
        ('include', '<', 'file2-yes'),
    ]

    substitution_expect = [
        ('include', '"', 'file3-yes'),
        ('include', '<', 'file4-yes'),
        ('include', '"', 'file5-yes'),
        ('include', '<', 'file6-yes'),
    ]

    ifdef_expect = [
        ('include', '"', 'file7-yes'),
        ('include', '"', 'file7-no'),
        ('include', '<', 'file8-no'),
        ('include', '<', 'file8-yes'),
    ]

    if_boolean_expect = [
        ('include', '"', 'file9-no'),
        ('include', '"', 'file9-yes'),
        ('include', '<', 'file10-yes'),
        ('include', '<', 'file10-no'),
        ('include', '"', 'file11-no-1'),
        ('include', '"', 'file11-no-2'),
        ('include', '"', 'file11-yes'),
        ('include', '<', 'file12-no-1'),
        ('include', '<', 'file12-yes'),
        ('include', '<', 'file12-no-2'),
        ('include', '"', 'file13-yes'),
        ('include', '"', 'file13-no-1'),
        ('include', '"', 'file13-no-2'),
        ('include', '<', 'file14-yes'),
        ('include', '<', 'file14-no-1'),
        ('include', '<', 'file14-no-2'),
    ]

    if_defined_expect = [
        ('include', '"', 'file15-yes'),
        ('include', '<', 'file16-no'),
        ('include', '<', 'file16-yes'),
        ('include', '"', 'file17-yes'),
        ('include', '<', 'file18-no'),
        ('include', '<', 'file18-yes'),
    ]

    expression_expect = [
        ('include', '"', 'file19-no'),
        ('include', '"', 'file19-yes'),
        ('include', '<', 'file20-no'),
        ('include', '<', 'file20-yes'),
        ('include', '"', 'file21-no'),
        ('include', '"', 'file21-yes'),
        ('include', '<', 'file22-yes'),
        ('include', '<', 'file22-no'),
        ('include', '"', 'file23-no'),
        ('include', '"', 'file23-yes'),
        ('include', '<', 'file24-yes'),
        ('include', '<', 'file24-no'),
        ('include', '"', 'file25-yes'),
        ('include', '"', 'file25-no'),
        ('include', '<', 'file26-yes'),
        ('include', '<', 'file26-no'),
        ('include', '"', 'file27-yes'),
        ('include', '"', 'file27-no'),
        ('include', '<', 'file28-no'),
        ('include', '<', 'file28-yes'),
        ('include', '"', 'file29-no'),
        ('include', '"', 'file29-yes'),
        ('include', '<', 'file30-yes'),
        ('include', '<', 'file30-no'),
    ]

    undef_expect = [
        ('include', '"', 'file31-yes'),
        ('include', '"', 'file31-no'),
        ('include', '<', 'file32-no'),
        ('include', '<', 'file32-yes'),
    ]

    macro_function_expect = [
        ('include', '"', 'file33-yes'),
        ('include', '<', 'file34-yes'),
        ('include', '"', 'file35-yes'),
        ('include', '<', 'file36-yes'),
        ('include', '"', 'file37-yes'),
        ('include', '<', 'file38-yes'),
        ('include', '"', 'file39-yes'),
        ('include', '<', 'file40-yes'),
    ]

    token_pasting_expect = [
        ('include', '"', 'file41-yes'),
        ('include', '<', 'file42-yes'),
    ]

if __name__ == '__main__':
    suite = unittest.TestSuite()
    tclasses = [ PreProcessorTestCase,
                 DumbPreProcessorTestCase,
               ]
    for tclass in tclasses:
        names = unittest.getTestCaseNames(tclass, 'test_')
        suite.addTests(map(tclass, names))
    if not unittest.TextTestRunner().run(suite).wasSuccessful():
        sys.exit(1)

