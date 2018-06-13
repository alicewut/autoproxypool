from settings import pool_max_count
from redisdb import RedisClient
from crawler import Crawler


class Getter():
	# 从互联网上爬取到的代理存入redis中
	def __init__(self):
		self.pool_max_count = pool_max_count
		self.redis = RedisClient()
		self.crawler = Crawler()
		
	def is_over_upperlimit(self):
		if self.redis.count() >= self.pool_max_count:
			return True
		else:
			return False
		
	def run(self):
		if not self.is_over_upperlimit():
			# print(self.crawler.__CrawlFuncCount__)
			for callback_label in range(self.crawler.__CrawlFuncCount__):
				callback = self.crawler.__CrawlFunc__[callback_label]
				proxies = self.crawler.get_proxy(callback)
				for proxy in proxies:
					print(proxy)
					self.redis.add(proxy)
					


if __name__ == '__main__':
	aa = Getter()
	aa.run()