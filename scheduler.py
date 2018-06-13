TESTER_CYCLE = 20
GETTER_CYCLE = 20
TESTER_ENABLED = True
GETTER_ENABLED = True
API_ENABLED =True

from multiprocessing import Process
from api import app
from getproxy import Getter
from proxyavailable import Tester
from settings import api_host, api_port
import time


class Scheduler():
	def scheduler_tester(self, cycle=TESTER_CYCLE):
		while True:
			tester = Tester()
			tester.run()
			time.sleep(cycle)
		
	def scheduler_getter(self, cycle=GETTER_CYCLE):
		while True:
			getter = Getter()
			getter.run()
			time.sleep(cycle)
	
	def scheduler_api(self):
		app.run(api_host, api_port)
	
	def run(self):
		print("代理池开始运行")
		if GETTER_ENABLED:
			getter_process = Process(target=self.scheduler_getter)
			getter_process.start()
			
		if TESTER_ENABLED:
			tester_process = Process(target=self.scheduler_tester)
			tester_process.start()
			
		if 	API_ENABLED:
			api_process = Process(target=self.scheduler_api)
			api_process.start()
			
if __name__ == '__main__':
	aa = Scheduler()
	aa.run()