import threading
import time

import pymongo
from schedule import Scheduler

from msic import config
from msic.common import utils
from msic.core.service import mongodb_service
from msic.proxy import proxy_strategy

TASK_INTERVAL = 60
FAILED_COUNT_BORDER = 10
MIN_PROXY_COUNT = 20


class ProxyPool(object):
	TABLE_NAME = 'proxy_pool'

	def __init__(self):
		self.collection = mongodb_service.get_collection(config.mongodb, self.TABLE_NAME)
		self.collection.create_index([('ip', pymongo.ASCENDING)], unique=True, sparse=True)

	# Singleton
	def __new__(cls, *args, **kwargs):
		if not hasattr(cls, '_instance'):
			org = super(ProxyPool, cls)
			cls._instance = org.__new__(cls, *args)
		return cls._instance

	def random_choice_proxy(self) -> str:
		proxy = self.collection.find().sort(
			[("failed_count", pymongo.ASCENDING), ("validity", pymongo.DESCENDING), ("response_speed", pymongo.ASCENDING),
			 ("update_time", pymongo.DESCENDING)])
		return proxy[0]['ip']

	def add_failed_time(self, ip):
		proxy = self.collection.find_one({'ip': ip})
		if proxy is not None:
			failed_count = proxy['failed_count'] + 1
			utils.log("ip: %s 失败次数+1 已失败次数%s次" % (ip, failed_count))
			if failed_count <= FAILED_COUNT_BORDER:
				try:
					self.collection.update_one({'ip': ip}, {"$set": {'update_time': utils.get_utc_time(), 'failed_count': failed_count}})
					utils.log("ip: %s 更新数据库失败次数" % ip)
				except:
					pass
			else:
				try:
					self.collection.delete_one({'ip': ip})
					utils.log("ip: %s 从数据库中删除" % ip)
				except:
					pass
		self.crawl_proxy_task()

	def crawl_proxy_task(self, check_num: bool = True):
		if check_num:
			count = self.collection.count()
			if count > MIN_PROXY_COUNT:
				utils.log("代理数大于%d不用获取新的ip" % MIN_PROXY_COUNT)
				return
		utils.log("开始抓取代理")
		proxy_list = proxy_strategy.crawl_proxy()
		utils.log("开始保存")
		for proxy in proxy_list:
			if not self.collection.find_one({'ip': proxy.ip}):
				self.collection.insert_one(proxy.__dict__)
				utils.log('保存了:' + proxy.ip)
		utils.log("保存结束")

	def check_ip_availability_task(self):
		proxy_list = self.collection.find()
		for proxy in proxy_list:
			ip = proxy['ip']
			start_time = time.time()
			response = utils.http_request('http://lwons.com/wx', timeout=10)
			is_success = response.status_code == 200
			response.close()
			if not is_success:
				try:
					self.collection.delete_one({'ip': ip})
				except:
					pass
				utils.log('Check ip %s FAILED' % ip)
			else:
				elapsed = round(time.time() - start_time, 4)
				try:
					self.collection.update_one({'ip': ip}, {"$set": {'update_time': utils.get_utc_time(), 'response_speed': elapsed, 'validity': True}})
				except:
					pass
				utils.log('Check ip %s SUCCESS' % ip)

	def start(self):
		self.collection.drop()
		self.crawl_proxy_task(False)

		def task():
			self.check_ip_availability_task()
			schedule = Scheduler()
			schedule.every(TASK_INTERVAL).minutes.do(self.check_ip_availability_task)

			while True:
				schedule.run_pending()
				time.sleep(1)

		thread = threading.Thread(target=task)
		thread.start()


proxy_pool = ProxyPool()
