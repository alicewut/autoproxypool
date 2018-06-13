"""
定义常用配置项
"""

# # redis 配置信息
# redis 数据库地址
redis_host = '192.168.12.139'

# redis 端口号
redis_port = 6379

# redis 密码
redis_passwd = '123456'

# redis 键名
redis_key = 'proxy'


# # 代理分数设置
max_score = 100
min_score = 0
initial_score = 10

# # 代理池代理数限制
pool_max_count = 50000


# #测试模块
# 测试地址
test_url = 'http://www.baidu.com'

# 合格的响应码
Valid_Status_Codes = [200]

# 每次测试量
BATCH_TEST_SIZE = 100


# api

api_host = '0.0.0.0'
api_port = 8080