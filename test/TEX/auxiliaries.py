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
Verify that sections of LaTeX output that use auxiliary files (a
bibliography in our configuration below) are consistent when re-run
after modifying the input file.

This checks for a bug that was triggered by the presence of auxiliary
files which were detected by SCons but then removed prior to invoking
TeX, causing the auxiliary sections to be excluded from the output.
That was fixed (courtesy Joel B. Mohler) by making all the relevant
auxiliary files Precious().

Test configuration courtesy Dmitry Mikhin.
"""

import TestSCons

test = TestSCons.TestSCons()

dvips = test.where_is('dvips')
latex = test.where_is('latex')

if not dvips or not latex:
    test.skip_test("Could not find dvips or latex; skipping test(s).\n")


test.subdir(['docs'])

test.write(['SConstruct'], """\
env = Environment(tools = ['pdftex', 'dvipdf', 'dvips', 'tex', 'latex'],
                  ENV = {},
                  BUILD_DIR = '#build/docs')

# Use 'duplicate=1' because LaTeX toolchain does not work properly for
# input/output files outside of the current directory

env.BuildDir('$BUILD_DIR', 'docs', duplicate=1)
env.SConscript('$BUILD_DIR/SConscript', exports = ['env'])
""")

test.write(['docs', 'SConscript'], """\
Import('env')
envc = env.Clone()

test_dvi = envc.DVI(source='test.tex')
test_ps = envc.PostScript(source='test.tex')
test_pdf = envc.PDF(source='test.tex')

envc.Default(test_dvi)
envc.Default(test_ps)
envc.Default(test_pdf)
""")

test.write(['docs', 'my.bib'], """\
@ARTICLE{Mikhin,
   author = "Dmitry {\uppercase{Y}u}. Mikhin",
   title = "Blah!",
   journal = "Some yellow paper",
   year = "2007",
   volume = "7",
   number = "3",
   pages = "1--2"
}
""")

tex_input = r"""\documentclass{article}

\title{BUG IN SCONS}

\author{Dmitry Yu. Mikhin}

\begin{document}

\maketitle


\begin{abstract}
\noindent A bug in BibTeX processing?
\end{abstract}


\section{The problem}

Provide a citation here: \cite{Mikhin}.


\bibliography{my}
\bibliographystyle{unsrtnat}

\end{document}
"""

test.write(['docs', 'test.tex'], tex_input)

test.run(stderr=None)

pdf_output_1 = test.read(['build', 'docs', 'test.pdf'])
ps_output_1 = test.read(['build', 'docs', 'test.ps'])

# Adding blank lines will cause SCons to re-run the builds, but the
# actual contents of the output files shouldn't be any different.
# This assumption won't work if it's ever used with a toolchain that does
# something to the output like put a commented-out timestamp in a header.
test.write(['docs', 'test.tex'], tex_input + "\n\n\n")

test.run(stderr=None)

pdf_output_2 = test.read(['build', 'docs', 'test.pdf'])
ps_output_2 = test.read(['build', 'docs', 'test.ps'])

test.fail_test(pdf_output_1 != pdf_output_2)
test.fail_test(ps_output_1 != ps_output_2)

test.pass_test()
