import threading
import time

import requests
from bs4 import BeautifulSoup
from requests.adapters import HTTPAdapter
from schedule import Scheduler

HEADERS = {
	'User-Agent': 'Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/38.0.2125.122 Safari/537.36',
	'Connection': 'keep-alive',
	'Content-Encoding': 'gzip',
	'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8'}

URL = 'http://www.xicidaili.com'
INTERVAL = 2
IP_LIST = []


class ProxyCrawler(object):
	@staticmethod
	def get_content(url: str) -> str:
		session = requests.Session()
		session.mount('https://', HTTPAdapter(max_retries=5))
		session.mount('http://', HTTPAdapter(max_retries=5))
		response = session.get(url, headers=HEADERS)
		return response.text

	@staticmethod
	def parse_content(content: str) -> []:
		ip = []
		soup = BeautifulSoup(content, 'html.parser')
		ip_list = soup.find('table', id='ip_list')
		ip_tr_list = ip_list.find_all('tr', limit=20)
		for index, ip_tr in enumerate(ip_tr_list):
			if index < 2:
				continue
			ip_td = ip_tr.find_all('td')
			address = ''
			port = ''
			is_high_quality = True
			for num, data in enumerate(ip_td):
				if num == 1:
					address = data.getText()
				elif num == 2:
					port = data.getText()
				# elif num == 6 or num == 7:
				# 	value = data.find('div', class_='bar').find('div').attrs['style']  # type:str
				# 	is_high_quality = is_high_quality and int(value.replace('width:', '').replace('%', '')) > 80
				elif num > 7:
					break
			if is_high_quality:
				ip.append(address + ':' + port)
		return ip

	@staticmethod
	def write_ip(ip_list: {}):
		del IP_LIST[:]
		for ip in ip_list:
			IP_LIST.append(ip)

	@staticmethod
	def check_proxy(ip: str, url: str = 'http://www.baidu.com') -> bool:
		proxies = {"http": ip}
		header = HEADERS
		try:
			req = requests.get(url, proxies=proxies, timeout=10, headers=header)
			if req.status_code == requests.codes.ok:
				return True
			else:
				return False
		except Exception as e:
			return False

	def check_ip_availability(self, url: str = 'http://www.baidu.com'):
		for ip in IP_LIST:
			if not ProxyCrawler.check_proxy(ip, url):
				IP_LIST.remove(ip)
				print('check ip %s FAILED' % ip)
			else:
				print('check ip %s SUCCESS' % ip)

	def run(self):
		print("reload proxy")
		content = self.get_content(URL)
		ip_list = self.parse_content(content)
		print("ip :%s" % ip_list)
		self.write_ip(ip_list)
		print("ip proxy:%s" % IP_LIST)


def start():
	def task():
		crawler = ProxyCrawler()
		schedule = Scheduler()

		schedule.every(INTERVAL).minutes.do(crawler.run)
		schedule.every(INTERVAL).minutes.do(crawler.check_ip_availability)

		crawler.run()
		crawler.check_ip_availability()
		while True:
			schedule.run_pending()
			time.sleep(1)

	thread = threading.Thread(target=task)
	thread.start()
