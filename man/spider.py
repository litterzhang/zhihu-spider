#!D:\python\python.exe
# -*- coding: utf-8 -*-

'知乎爬虫程序入口，负责登录，维护会话'

__author__ = 'litter_zhang'

import time
import json
import requests

from common import *

class ZhihuSpider(object):
	"""知乎爬虫类，内部维护了与知乎的会话，可以使用cookies或者账户密码登录"""
	def __init__(self, cookies=None):
		super(ZhihuSpider, self).__init__()
		
		self._session = requests.Session()
		self._session.headers.update(Default_Header)

		if cookies is not None:
			assert isinstance(cookies, str)
			self.login_with_cookies(cookies)
		else:
			self.login_in_terminal()

	@staticmethod
	def _get_captcha_url():
		return Captcha_URL_Prefix + str(int(time.time() * 1000))

	def get_captcha(self):
		"""获取验证码数据。

		:return: 验证码图片数据。
		:rtype: bytes
		"""
		# some unbelievable zhihu logic
		self._session.get(Zhihu_URL)
		# data = {'email': '', 'password': '', 'remember_me': 'true'}
		# self._session.post(Login_URL, data=data)

		r = self._session.get(self._get_captcha_url())
		return r.content

	def login(self, email, password, captcha):
		"""登陆知乎.

		:param str email: 邮箱
		:param str password: 密码
		:param str captcha: 验证码
		:return:
			======== ======== ============== ====================
			元素序号 元素类型 意义           说明
			======== ======== ============== ====================
			0        int      是否成功       0为成功，1为失败
			1        str      失败原因       登录成功则为空字符串
			2        str       cookies字符串 登录失败则为空字符串
			======== ======== ============== ====================

		:rtype: (int, str, str)
		"""
		data = {'email': email, 'password': password, 'remember_me': 'true', 'captcha': captcha}
		r = self._session.post(Login_URL, data=data)

		#print(r.json())
		j = r.json()
		code = int(j['r'])
		message = j['msg'] if code == 0 else j['data']
		cookies_str = json.dumps(self._session.cookies.get_dict()) if code == 0 else ''
		return code, message, cookies_str

	def login_with_cookies(self, cookies):
		pass

	def login_in_terminal(self, cookies_file='cookies'):
		"""不使用cookies，在终端中根据提示登陆知乎

		:return: 如果成功返回cookies字符串
		:rtype: str
		"""
		print('====== zhihu login =====')

		email = input('email: ')
		password = input('password: ')

		captcha_data = self.get_captcha()
		with open('captcha.gif', 'wb') as f:
			f.write(captcha_data)

		print('please check captcha.gif for captcha')
		captcha = input('captcha: ')
		#os.remove('captcha.gif')

		print('====== logging.... =====')

		code, msg, cookies = self.login(email, password, captcha)

		if code == 0:
			print('login successfully')
			# save cookies
			if cookies:
				with open(cookies_file, 'w') as f:
					f.write(cookies)
				print('cookies file created.')
			else:
				print('can\'t create cookies.')
		else:
			print('login failed, reason: {0}'.format(msg))
		
	
		return cookies


		

