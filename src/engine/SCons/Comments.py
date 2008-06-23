"""SCons.Comments

Comments stripping function + control function (temporarily?).
"""

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
import SCons.Util

SIGS_DIFFER = 3
SIGS_EQUAL = 2
SIGS_WHOLE = 1 # count md5 sum for whole file

def Stripper(dependency, target, prev_ni):
    """Main control function for comments stripping framework.
    According to the target's type Stripper() decides what to
    strip from the dependency file."""

    d, t = dependency, target
    dx, tx = d.suffix, t.suffix

    if (dx == '.c' or dx == '.h') and tx == '.o':
        code = CComments(str(dependency))
        if not dependency.rexists():
            return SIGS_WHOLE

        csig = SCons.Util.MD5signature(code)
        dependency.ninfo.csig = csig #psig = psig
        try:
            if dependency.ninfo.csig != prev_ni.csig:#psig != prev_ni.psig:
                return SIGS_DIFFER
            else:
                return SIGS_EQUAL
        except AttributeError:
            return SIGS_WHOLE
    return SIGS_WHOLE


def Code(filename, comment_char = '#'):
    """Strip the source code from the file and return comments.
    
    Open the file 'filename', get the contents, strip the code
    (treat everything between 'comment_char' sign and a new line
    as a comment), and return comments.
    
    Default for 'comment_char' is '#'."""

    try:
        f = open(filename, 'rb')
    except IOError:
        return ''
    
    txt = f.read()
    f.close()

    i = 0
    len_max = len(txt)
    buf = []
    single_quot = False
    double_quot = False
    metachars = 0
    while i < len_max:
        quoting = single_quot or double_quot
        # slash within a quote
        if quoting and txt[i] == '\\':
            metachars += 1
        # escaped quote
        elif quoting and txt[i] == ('"' or '\'') and metachars % 2:
            metachars = 0
        # opening/closing quote - turn the quoting on/off
        elif txt[i] == '\'' and not metachars % 2:
            if single_quot:
                single_quot = False
            else:
                single_quot = True
        elif txt[i] == '"' and not metachars % 2:
            if double_quot:
                double_quot = False
            else:
                double_quot = True

        # add the comment to the buffer
        if txt[i] == comment_char and not (single_quot or double_quot):
            while i < len_max and txt[i] != '\n':
                if not (txt[i] == ' ' or txt[i] == '\n'):
                    buf.append(txt[i])
                i += 1
        i += 1

    return ''.join(buf)


def Comments(filename, comment_char = '#'):
    """Strip the comments from the file and return source code.
    
    Open the file 'filename', get the contents, strip the comments
    (treat everything after 'comment_char' sign as a comment),
    and return source code.
    
    Default for 'comment_char' is '#'."""

    try:
        f = open(filename, 'rb')
    except IOError:
        return ''
    
    txt = f.read()
    f.close()

    i = 0
    len_max = len(txt)
    buf = []
    single_quot = False
    double_quot = False
    metachars = 0
    while i < len_max:
        quoting = single_quot or double_quot
        # slash within a quote
        if quoting and txt[i] == '\\':
            metachars += 1
        # escaped quote
        elif quoting and txt[i] == ('"' or '\'') and metachars % 2:
            metachars = 0
        # opening/closing quote - turn the quoting on/off
        elif txt[i] == '\'' and not metachars % 2:
            if single_quot:
                single_quot = False
            else:
                single_quot = True
        elif txt[i] == '"' and not metachars % 2:
            if double_quot:
                double_quot = False
            else:
                double_quot = True

        # strip the comment
        if txt[i] == comment_char and not (single_quot or double_quot):
            while i < len_max and txt[i] != '\n':
                i += 1
        # add to the buffer
        else:
            if not (txt[i] == ' ' or txt[i] == '\n'):
                buf.append(txt[i])
        i += 1

    return ''.join(buf)


def CCode(filename):
    """Strip the code from the file and return comments.
    
    Open the file 'filename', get the contents, strip the comments
    and return source code.
    
    Works for '//' and '/* */' comments."""

    try:
        f = open(filename, 'rb')
    except IOError:
        return ''
    
    txt = f.read()
    f.close()

    i = 0
    len_max = len(txt)
    buf = []
    quot = False
    metachars = 0
    while i < len_max:
        if quot and txt[i] == '\\':
            metachars += 1
        elif txt[i] != '"':
            metachars = 0

        # turn the quoting on/off
        if txt[i] == '"' and not metachars % 2:
            if quot:
                quot = False
            else:
                quot = True

        # add '//' comment to the buffer
        if txt[i] == '/' and txt[i+1] == '/' and not quot:
            while i < len_max and txt[i] != '\n':
                if not (txt[i] == ' ' or txt[i] == '\n'):
                    buf.append(txt[i])
                i += 1
        # add '/* */' comment to the buffer
        elif txt[i] == '/' and txt[i+1] == '*' and not quot:
            while i+1 < len_max:
                if txt[i] == '*' and txt[i+1] == '/':
                    buf.append(txt[i]); buf.append(txt[i+1])
                    break
                if not (txt[i] == ' ' or txt[i] == '\n'):
                    buf.append(txt[i])
                i += 1
        i+=1
    return ''.join(buf)


def CComments(filename):
    """Strip C-like comments from the file and return source code.
    
    Open the file 'filename', get the contents, strip the comments
    and return source code.
    
    Works for '//' and '/* */' comments."""

    try:
        f = open(filename, 'rb')
    except IOError:
        return ''
    
    txt = f.read()
    f.close()

    i = 0
    len_max = len(txt)
    buf = []
    while i < len_max:
        # add quote to the buffer
        if txt[i] == '"':
            metachars = 0
            buf.append(txt[i])
            i += 1
            try:
                while i < len_max:
                    if txt[i] == '\\':
                        metachars += 1
                        buf.append(txt[i])
                        i += 1
                        continue
                    elif txt[i] == '"':
                        if metachars % 2:
                            buf.append(txt[i])
                            i += 1
                            metachars = 0
                            continue
                        buf.append(txt[i])
                        i += 1
                        break
                    buf.append(txt[i])
                    i += 1
                    metachars = 0
            except IndexError:
                continue

        # strip '//' comment
        if txt[i] == '/' and txt[i+1] == '/':
            while i < len_max and txt[i] != '\n':
                i += 1
        # strip '/* */' comment
        elif txt[i] == '/' and txt[i+1] == '*':
            while i+1 < len_max:
                if txt[i] == '*' and txt[i+1] == '/':
                    i += 1
                    break
                i += 1
        # add the code to the buffer
        else:
            if not (txt[i] == ' ' or txt[i] == '\n'):
                buf.append(txt[i])

        i += 1

    return ''.join(buf)


def DCode(filename):
    """Strip the code from the file and return comments.
    
    Open the file 'filename', get the contents, strip the comments
    and return source code.
    
    Works for '//', '/* */' and '/+ +/' comments."""

    try:
        f = open(filename, 'rb')
    except IOError:
        return ''
    
    txt = f.read()
    f.close()

    i = 0
    len_max = len(txt)
    buf = []
    quot = False
    metachars = 0
    while i < len_max:
        if quot and txt[i] == '\\':
            metachars += 1
        elif txt[i] != '"':
            metachars = 0

        # turn the quoting on/off
        if txt[i] == '"' and not metachars % 2:
            if quot:
                quot = False
            else:
                quot = True

        # add '//' comment to the buffer
        if txt[i] == '/' and txt[i+1] == '/' and not quot:
            while i < len_max and txt[i] != '\n':
                if not (txt[i] == ' ' or txt[i] == '\n'):
                    buf.append(txt[i])
                i += 1
            metachars = 0
        # add '/* */' comment to the buffer
        elif txt[i] == '/' and txt[i+1] == '*' and not quot:
            while i+1 < len_max:
                if txt[i] == '*' and txt[i+1] == '/':
                    buf.append(txt[i]); buf.append(txt[i+1])
                    break
                if not (txt[i] == ' ' or txt[i] == '\n'):
                    buf.append(txt[i])
                i += 1
            metachars = 0
        # add '/+ +/' comment to the buffer
        elif txt[i] == '/' and txt[i+1] == '+' and not quot:
            while i < len_max:
                if txt[i] == '+' and txt[i+1] == '/':
                    buf.append(txt[i]); buf.append(txt[i+1])
                    break
                if not (txt[i] == ' ' or txt[i] == '\n'):
                    buf.append(txt[i])
                i += 1
            metachars = 0
        i+=1
    return ''.join(buf)


def DComments(filename):
    """Strip C-like comments from the file and return source code.
    
    Open the file 'filename', get the contents, strip the comments
    and return source code.
    
    Works for '//' and '/* */' comments."""

    try:
        f = open(filename, 'rb')
    except IOError:
        return ''
    
    txt = f.read()
    f.close()

    i = 0
    len_max = len(txt)
    buf = []
    while i < len_max:
        # add quote to the buffer
        if txt[i] == '"':
            metachars = 0
            buf.append(txt[i])
            i += 1
            try:
                while i < len_max:
                    if txt[i] == '\\':
                        metachars += 1
                        buf.append(txt[i])
                        i += 1
                        continue
                    elif txt[i] == '"':
                        if metachars % 2:
                            buf.append(txt[i])
                            i += 1
                            metachars = 0
                            continue
                        buf.append(txt[i])
                        i += 1
                        break
                    buf.append(txt[i])
                    i += 1
                    metachars = 0
            except IndexError:
                continue

        # strip /+ +/ comments
        if txt[i] == '/' and txt[i+1] == '+':
            while i < len_max:
                if txt[i] == '+' and txt[i+1] == '/':
                    i += 2
                    break
                i += 1
        # strip // comments
        elif txt[i] == '/' and txt[i+1] == '/':
            while i < len_max and txt[i] != '\n':
                i += 1
        # strip /* */ comments
        elif txt[i] == '/' and txt[i+1] == '*':
            while i+1 < len_max:
                if txt[i] == '*' and txt[i+1] == '/':
                    i += 1
                    break
                i += 1
        # add to buffer
        else:
            if not (txt[i] == ' ' or txt[i] == '\n'):
                buf.append(txt[i])
        i += 1

    return ''.join(buf)

