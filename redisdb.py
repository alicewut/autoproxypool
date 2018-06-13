import redis
from settings import redis_host, redis_port, redis_passwd, redis_key
from settings import max_score, min_score, initial_score
from error import PoolEmptyError
import random

class RedisClient(object):
	def __init__(self, host=redis_host, port=redis_port, passwd=redis_passwd):
		self.db = redis.StrictRedis(host=host,port=port,password=passwd,decode_responses=True)

	def add(self, proxy,score=initial_score):
		"""
		将新的代理添加至redis中，并附分数初值10
		利用redis中的值的分数，作为代理的有效分数
		:param proxy: 代理，"host:port" 格式
		:param score: 分数，初始值为10
		:return:
		"""
		# 判断当这个有序集redis_key中proxy的score值不存在时,
		# 将这个proxy和其score值加入到这个有续集redis_key中
		if not self.db.zscore(redis_key, proxy):
			return self.db.zadd(redis_key, score, proxy)
	
	def random(self):
		"""
		随机获取有效代理，默认在score值为100的中随机取一个，若不存在则按最高排名获取，否则手动抛出异常
		:return: 有效的代理
		"""
		# 首先获取score为100的代理
		res = self.db.zrangebyscore(redis_key, max_score, max_score)
		if len(res):
			return random.choice(res)
		else:
			res = self.db.zrevrange(redis_key, 0, 100)
			if len(res):
				return random.choice(res)
			else:
				raise PoolEmptyError
			
	def count(self):
		"""
		:return: 返回某个key 的基数
		"""
		return self.db.zcard(redis_key)
	
	def max(self, proxy):
		"""
		
		:return: 设置某个代理的socre 为100，因为原值已经被取走，在redis中不存在，故直接新添加即可
		"""
		print('代理', proxy,'可用。设置为：', max_score)
		return self.db.zadd(redis_key, max_score, proxy)
		
	def decrease(self, proxy):
		"""
		指定代理的 score 减1，若当前的score已经小于等于最小值，则删除
		:return:
		"""
		current_score = self.db.zscore(redis_key, proxy)
		if current_score and current_score > min_score:
			print('代理', proxy, '当前分数', current_score, '减1')
			return self.db.zincrby(redis_key, proxy, -1)
		else:
			print('代理', proxy, '当前分数', current_score, '移除')
			return self.db.zrem(redis_key, proxy)
	
	def all(self):
		"""
		:return: 返回在一个范围内的（min, max）的序列
		"""
		return self.db.zrangebyscore(redis_key, min_score, max_score)
	
	def batch(self, start, stop):
		"""
		:return: 返回指定范围内的代理列表
		"""
		return self.db.zrevrange(redis_key, start, stop)
	
	
if __name__ == '__main__':
	aa = RedisClient()
	print(aa.random())