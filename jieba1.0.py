#encoding=utf8

import sys
import os
import jieba

if not os.path.exists(sys.argv[1]):
    sys.exit(0)

jieba.set_dictionary('dict.txt.big')

content = open(sys.argv[1], 'rb').read()

print "Input：", content

words = jieba.cut(content, cut_all=False)

print "Output 精確模式 Full Mode："


f = open('{0}_word.txt'.format(sys.argv[1]), 'w')
for word in words:
	print (word)
	f.write(word.encode('utf-8'))
	f.write('\n')
f.close()
