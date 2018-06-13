from common import getPage
from lxml import etree


class ProxyMetaclass(type):
	def __new__(cls, name, bases, attrs):
		count = 0
		attrs['__CrawlFunc__'] = []
		for k,v in attrs.items():
			if 'crawl_' in k:
				attrs['__CrawlFunc__'].append(k)
				count += 1
		attrs['__CrawlFuncCount__'] = count
		return type.__new__(cls, name, bases, attrs)
		
 
# 定义爬虫类
class Crawler(object, metaclass=ProxyMetaclass):
	def get_proxy(self, callback):
		proxies = []
		for proxy in eval("self.{}()".format(callback)):
			print('获取到代理：', proxy)
			proxies.append(proxy)
		return proxies
			
		
	
	
	def crawl_daili66(self, page_count=10):
		"""
		爬取66代理数据
		:return: host:port
		"""
		# 66代理网站分页数据，n.html 即可.页码从1开始
		base_url = 'http://www.66ip.cn/{}.html'
		urls = [base_url.format(page) for page in range(2, page_count+1)]
		for url in urls:
			print('正在爬取：', url)
			html = getPage(url)
			if html:
				print('开始解析')
				# 使用xpath解析页面源代码
				html = etree.HTML(html)
				tr_list = html.xpath('//div[@id="main"]//div[@align="center"]/table//tr')
				
				for tr in tr_list[1:]:
					host = tr.xpath('./td[1]/text()')[0]
					port = tr.xpath('./td[2]/text()')[0]
					yield':'.join([host, port])


if __name__ == '__main__':
	res = Crawler()
	print(res.crawl_daili66())