"""
jieba 的命令行接口
使用方法：
    python -m jieba "hello,世界"
"""
import jieba
import sys

from ._compat import *
from argparse import ArgumentParser

# jieba 的命令行
parser = ArgumentParser(usage="%s -m jieba [options] filename" % sys.executable,
                        description="Jieba command line interface.", epilog="If no filename specified, use STDIN instead.")

# 切分标记符号
parser.add_argument("-d", "--delimiter", metavar="DELIM", default=' / ',
                    nargs='?', const=' ',
                    help="use DELIM instead of ' / ' for word delimiter; or a space if it is used without DELIM")
# 词性标注
parser.add_argument("-p", "--pos", metavar="DELIM", nargs='?', const='_',
                    help="enable POS tagging; if DELIM is specified, use DELIM instead of '_' for POS delimiter")

# 词典
parser.add_argument("-D", "--dict", help="use DICT as dictionary")

# 用户词典
parser.add_argument("-u", "--user-dict",
                    help="use USER_DICT together with the default dictionary or DICT (if specified)")

# 全切分模式
parser.add_argument("-a", "--cut-all",
                    action="store_true", dest="cutall", default=False,
                    help="full pattern cutting (ignored with POS tagging)")

# 不适用 hmm 算法
parser.add_argument("-n", "--no-hmm", dest="hmm", action="store_false",
                    default=True, help="don't use the Hidden Markov Model")

# 安静模式，不输出加载词典等信息
parser.add_argument("-q", "--quiet", action="store_true", default=False,
                    help="don't print loading messages to stderr")

# 输出 jieba 版本信息
parser.add_argument("-V", '--version', action='version',
                    version="Jieba " + jieba.__version__)

# 想要切分的文件
parser.add_argument("filename", nargs='?', help="input file")

# 获取所有的输入参数
args = parser.parse_args()

# loging 的等级
# 默认是 logging.DEBUG
if args.quiet:
    jieba.setLogLevel(60)

# 若需要词性标记则，导入 posseg，并获取词性标记的标注符号
if args.pos:
    import jieba.posseg
    posdelim = args.pos

    # 定义需要词性标记时的，切分函数
    # 默认 启用 HMM 算法
    def cutfunc(sentence, _, HMM=True):
        for w, f in jieba.posseg.cut(sentence, HMM):
            yield w + posdelim + f
# 若不进行词性标记将切分函数设为默认的 jieba.cut
else:
    cutfunc = jieba.cut

# 获得分词标记符号
# text_type 在 python3 中对应于 str
# 在python2 中对应于 unicde
delim = text_type(args.delimiter)

# 获得是否做全切分的标记
cutall = args.cutall

# 获得是否使用 hmm 算法
hmm = args.hmm

# 如果命令行输入了文件名则读入该文件
# 如果命令行直接输入了文本则读入文本
fp = open(args.filename, 'r') if args.filename else sys.stdin

# 如果指定了词典则使用该词典进行初始化
# 如果没有指定则使用默认的词典进行初始化
if args.dict:
    jieba.initialize(args.dict)
else:
    jieba.initialize()

# 加载用户自定义的词典
if args.user_dict:
    jieba.load_userdict(args.user_dict)

# 读入文件问容
ln = fp.readline()
while ln:
    # 删除空行
    ln = ln.rstrip('\r\n')

    # 切分
    result = delim.join(cutfunc(ln, cutall, hmm))

    # python 2
    if PY2:
        result = result.encode(default_encoding)

    # 打印
    print(result)
    ln = fp.readline()

fp.close()
