import sys

sys.path.append('../')

import jieba

c = jieba.Tokenizer()
f = c.get_dict_file()
print(f)
d = c.gen_pfdict(f)

print(d)
