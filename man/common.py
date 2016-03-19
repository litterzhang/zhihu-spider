#!D:\python\python.exe
# -*- coding: utf-8 -*-

'知乎爬虫程序常用信息'

__author__ = 'litter_zhang'

import re

Default_Header = {
	'X-Requested-With': 'XMLHttpRequest',
	'Referer': 'http://www.zhihu.com',
	'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:39.0) Gecko/20100101 Firefox/39.0',
	'Host': 'www.zhihu.com'}
Zhihu_URL = 'https://www.zhihu.com'
Login_URL_EMAIL = Zhihu_URL + '/login/email'
Login_URL_PHONE = Zhihu_URL + '/login/phone_num'
Captcha_URL_Prefix = Zhihu_URL + '/captcha.gif?r='
Get_Profile_Card_URL = Zhihu_URL + '/node/MemberProfileCardV2'

re_email = re.compile(r'^.*@.*\..*$')
re_phone = re.compile(r'^[0-9]{11}$')

re_question_url = re.compile(r'^https?://www\.zhihu\.com/question/(\d+)/?')
re_people_url = re.compile(r'^https?://www\.zhihu\.com/people/([^/]+)/?')
re_collection_url = re.compile(r'^https?://www\.zhihu\.com/collection/(\d+)/?')
re_zhuanlan_url = re.compile(r'^https?://zhuanlan\.zhihu\.com/([^/]+)/?')
re_topic_url = re.compile(r'^https?://www\.zhihu\.com/topic/(\d+)/?')
re_explore_url = re.compile(r'^https?://www\.zhihu\.com/explore/?')
re_roundtable_url = re.compile(r'^https?://www\.zhihu\.com/roundtable/([^/]+)/?')
re_search_url = re.compile(r'^https?://www\.zhihu\.com/search')

def url_type(url):
	url = url.split('#', 1)[0]

	if re_question_url.match(url):
		return 'question', url
	elif re_people_url.match(url):
		return 'people', url
	elif re_collection_url.match(url):
		return 'collection', url
	elif re_zhuanlan_url.match(url):
		return 'zhuanlan', url
	elif re_topic_url.match(url):
		return 'topic', url
	elif re_explore_url.match(url):
		return 'explore', url
	elif re_roundtable_url.match(url):
		return 'roundtable', url
	elif re_search_url.match(url):
		return 'search', url
	else:
		return 'none', url