import sys

from utils import *
sys.path.append('../')

import jieba


string = 'Hello,世界！'
result = jieba.cut(string)

string2 = '我爱北京天安门'
result2 = jieba.cut(string2)
jb_print(result)
jb_print(result2)
