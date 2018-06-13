import requests
from requests.exceptions import ConnectionError
from fake_useragent import UserAgent
import random

def getPage(url):
	"""
	实现获取页面的源代码的功能
	:param url: 请求页面的路由
	:return: 请求成功返回页面源代码，否则返回None
	"""
	header = {
		'User-Agent': UserAgent().random
	}
	response = requests.get(url, headers=header)
	try:
		if response.status_code == requests.codes.ok:
			response.encoding = response.apparent_encoding
			return response.text
	except ConnectionError:
		return None
	
	
if __name__ == '__main__':
	res = getPage('http://www.66ip.cn/1.html')
	print(res)