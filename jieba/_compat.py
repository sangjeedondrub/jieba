# -*- coding: utf-8 -*-
import os
import sys

# TODO what does this part do ?
try:
    import pkg_resources
    get_module_res = lambda *res: pkg_resources.resource_stream(__name__,
                                                                os.path.join(*res))
except ImportError:
    get_module_res = lambda *res: open(os.path.normpath(os.path.join(
        os.getcwd(), os.path.dirname(__file__), *res)), 'rb')

# 是否为python 2 版本
PY2 = sys.version_info[0] == 2

# 默认的系统编码
default_encoding = sys.getfilesystemencoding()

# python2 和 python3 统一处理
if PY2:
    text_type = unicode
    string_types = (str, unicode)

    def iterkeys(d): return d.iterkeys()

    def itervalues(d): return d.itervalues()

    def iteritems(d): return d.iteritems()

else:
    text_type = str
    string_types = (str,)
    xrange = range

    def iterkeys(d): return iter(d.keys())

    def itervalues(d): return iter(d.values())

    def iteritems(d): return iter(d.items())


# 解码字符串
def strdecode(sentence):
    if not isinstance(sentence, text_type):
        try:
            sentence = sentence.decode('utf-8')
        except UnicodeDecodeError:
            sentence = sentence.decode('gbk', 'ignore')
    return sentence


def resolve_filename(f):
    try:
        return f.name
    except AttributeError:
        return repr(f)
