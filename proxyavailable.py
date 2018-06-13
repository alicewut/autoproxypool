from redisdb import RedisClient
from settings import test_url, Valid_Status_Codes, BATCH_TEST_SIZE
import aiohttp, asyncio, time, sys

class Tester(object):
	def __init__(self):
		self.redis = RedisClient()
		
		
	async def test_single_proxy(self, proxy):
		conn = aiohttp.TCPConnector(verify_ssl=False)
		async with aiohttp.ClientSession(connector=conn) as session:
			try:
				if isinstance(proxy, bytes):
					proxy = proxy.decode('utf-8')
				real_proxy = 'http://' + proxy
				print('正在测试', proxy)
				async with session.get(test_url, proxy=real_proxy,timeout=15,allow_redirects=False) as response:
					if response.status in Valid_Status_Codes:
						self.redis.max(proxy)
						print('该代理可用：', proxy)
					else:
						self.redis.decrease(proxy)
						print('该代理的请求响应码异常：', proxy)
			except (aiohttp.ClientError, aiohttp.ClientProxyConnectionError, asyncio.TimeoutError):
				self.redis.decrease(proxy)
				print('该代理的请求失败：', proxy)
		
			
	def run(self):
		"""
		测试主函数
		:return: None
		"""
		
		try:
			proxies_count = self.redis.count()
			print('当前剩余代理数：', proxies_count)
			for start in range(0, proxies_count, BATCH_TEST_SIZE):
				stop = min(start + BATCH_TEST_SIZE, proxies_count)
				print('正在测试第', start, '-', (stop + 1), '个代理')
				test_proxies = self.redis.batch(start, stop)
				loop = asyncio.get_event_loop()
				tasks = [self.test_single_proxy(proxy) for proxy in test_proxies]
				loop.run_until_complete(asyncio.wait(tasks))
				sys.stdout.flush()
				time.sleep(5)
			
		except Exception as e:
			print('测试器发生错误', e.args)
			
if __name__ == '__main__':
	aa = Tester()
	aa.run()
			