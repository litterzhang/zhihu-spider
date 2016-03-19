#!D:\python\python.exe
# -*- coding: utf-8 -*-

'知乎爬虫程序入口，负责登录，维护会话'

__author__ = 'litter_zhang'

import os
import time
import json
import requests
import importlib

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

	def get_captcha_and_xsrf(self):
		"""获取验证码数据。

		:return: 验证码和xsrf图片数据。
		:rtype: bytes
		"""
		# some unbelievable zhihu logic
		self._session.get(Zhihu_URL)

		#get _xsrf in cookies
		xsrf = self._session.cookies.get_dict().get('_xsrf', '')

		# data = {'email': '', 'password': '', 'remember_me': 'true'}
		# self._session.post(Login_URL, data=data)

		#get captcha from generate url
		captcha_url = Captcha_URL_Prefix + str(int(time.time() * 1000))
		r = self._session.get(captcha_url)

		return r.content, xsrf

	def login(self, account_type, account, password, xsrf, captcha):
		"""登陆知乎.

		:param int account_type: 用户名类型
		:param str account: 用户名(邮箱或者手机号)
		:param str password: 密码
		:param str xsrf: _xsrf
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

		# create login url and data
		login_url = Login_URL_EMAIL
		if account_type is 0:
			login_url = Login_URL_EMAIL
			data = {'email': account, 'password': password, '_xsrf': xsrf, 'remember_me': 'true', 'captcha': captcha}
		else:
			login_url = Login_URL_PHONE
			data = {'phone_num': account, 'password': password, '_xsrf': xsrf, 'remember_me': 'true', 'captcha': captcha}
		r = self._session.post(login_url, data=data)

		# get login result
		j = r.json()
		code = int(j['r'])
		message = j['msg'] if code == 0 else j['data']
		cookies_str = json.dumps(self._session.cookies.get_dict()) if code == 0 else ''
		return code, message, cookies_str

	def login_with_cookies(self, cookies):
		"""使用cookies文件或字符串登录知乎

		:param str cookies:
			============== ===========================
			参数形式       作用
			============== ===========================
			文件名         将文件内容作为cookies字符串
			cookies字符串  直接提供cookies字符串
			============== ===========================
		:return: 无
		:rtype: None
		"""
		if os.path.isfile(cookies):
			with open(cookies) as f:
				cookies = f.read()
				cookies_dict = json.loads(cookies)
				self._session.cookies.update(cookies_dict)
		else:
			print('cookies file is not correct')

	def login_in_terminal(self, cookies_file='cookies'):
		"""不使用cookies，在终端中根据提示登陆知乎

		:return: 如果成功返回cookies字符串
		:rtype: str
		"""
		print('====== zhihu login =====')

		account = input('account: ')
		password = input('password: ')

		r_phone = re_phone.match(account)
		r_email = re_email.match(account)

		# check what the account is
		account_type = 0
		if r_email:
			account_type = 0
		elif r_phone:
			account_type = 1
		else:
			account_type = 2

		if account_type is 2:
			print('account check error[local]')
			return None


		captcha_data, xsrf = self.get_captcha_and_xsrf()
		with open('captcha.gif', 'wb') as f:
			f.write(captcha_data)

		print('please check captcha.gif for captcha')
		captcha = input('captcha: ')
		#os.remove('captcha.gif')

		print('====== logging.... =====')

		code, msg, cookies = self.login(account_type, account, password, xsrf, captcha)

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

	def load(self, url):
		url_t, url = url_type(url)
		
		if not url_t:
			print('url uncorrect')
			return None
		url_t_module = importlib.import_module(url_t)

		url_t_module.printer()


		

