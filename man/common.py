#!D:\python\python.exe
# -*- coding: utf-8 -*-

'知乎爬虫程序常用信息'

__author__ = 'litter_zhang'

Default_Header = {
	'X-Requested-With': 'XMLHttpRequest',
	'Referer': 'http://www.zhihu.com',
	'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:39.0) Gecko/20100101 Firefox/39.0',
	'Host': 'www.zhihu.com'}
Zhihu_URL = 'https://www.zhihu.com'
Login_URL = Zhihu_URL + '/login/email'
Captcha_URL_Prefix = Zhihu_URL + '/captcha.gif?r='
Get_Profile_Card_URL = Zhihu_URL + '/node/MemberProfileCardV2'