#!D:\python\python.exe
# -*- coding: utf-8 -*-

'分词测试'

__author__ = 'litter_zhang'

# import jieba

# seg_list = jieba.cut('本法是婚姻家庭关系的基本准则。', cut_all=True)
# print('/'.join(seg_list))

import jieba.posseg as pseg

words = pseg.cut('禁止包办、买卖婚姻和其他干涉婚姻自由的行为。')

for w in words:
	print(w.word, w.flag)