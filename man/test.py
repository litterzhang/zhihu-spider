#!D:\python\python.exe
# -*- coding: utf-8 -*-

'知乎爬虫程序测试'

__author__ = 'litter_zhang'

from spider import ZhihuSpider

spider = ZhihuSpider(cookies='cookies')

spider.load('https://www.zhihu.com/question/41450532#answer-31952471')