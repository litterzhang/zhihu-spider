#!D:\python\python.exe
# -*- coding: utf-8 -*-

'爬取分类为question的url'

__author__ = 'litter_zhang'

import requests
from urllib.parse import urljoin

from common import *

def url_type(url):
	url_t = 0
	if re_question_url_main.match(url):
		url_t = 0
	elif re_question_url_followers.match(url):
		url_t = 1
	elif re_question_url_answer.match(url):
		url_t = 2
	elif re_question_url_log.match(url):
		url_t = 3
	else:
		url_t = -1
	return url_t

class Question(object):
	"""docstring for Question"""
	def __init__(self, url, session=None):
		super(Question, self).__init__()

		self.url = url
		# print(session.cookies.get_dict())
		if session:
			self._session = session
		else:
			self._session = requests.Session()
		
		
	def load_question_main(self):
		# r = self._session.get(self.url)
		
		soup = BeautifulSoup(open('question'))

		# with open('question', 'w') as f:
		# 	f.write(r.text)
		
		question_id = soup.find(id='zh-single-question-page').attrs['data-urltoken']
		
		followers_area = soup.find(attrs={'class': 'zh-question-followers-sidebar'})
		followers_url = urljoin(self.url, followers_area.find(attrs={'class': 'zg-gray-normal'}).find('a').attrs['href'])
		followers_num = followers_area.find(attrs={'class': 'zg-gray-normal'}).find('strong').text
		followers_users = [{'username': it.attrs['title'], 'url': urljoin(self.url, it.attrs['href']), 'avatar': it.find('img').attrs['src']} for it in followers_area.find(attrs={'class': 'list'}).find_all('a')]

		print(followers_users)

	def load_question_followers(self):
		pass

	def load_question_answer(self):
		pass

	def load_question_log(self):
		pass

	def load(self):
		url_t = url_type(self.url)
		
		if url_t is 0:
			self.load_question_main()
		elif url_t is 1:
			self.load_question_followers()
		elif url_t is 2:
			self.load_question_answer()
		elif url_t is 3:
			self.load_question_log()
		else:
			return -1, 'url type error'



