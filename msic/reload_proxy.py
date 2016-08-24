from bs4 import BeautifulSoup
from requests.adapters import HTTPAdapter
import requests
import time
import threading
from schedule import Scheduler
from msic import proxy

HEADERS = {
	'User-Agent': 'Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/38.0.2125.122 Safari/537.36',
	'Connection': 'keep-alive',
	'Content-Encoding': 'gzip',
	'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8'}

URL = 'http://www.xicidaili.com/'

IP_LIST = proxy.FREE_PROXIES


class ProxyCrawler(object):
	@staticmethod
	def get_content(url: str) -> str:
		session = requests.Session()
		session.mount('https://', HTTPAdapter(max_retries=10))
		session.mount('http://', HTTPAdapter(max_retries=10))
		response = session.get(url, headers=HEADERS)
		return response.text

	@staticmethod
	def parse_content(content: str) -> []:
		ip = []
		soup = BeautifulSoup(content, 'html.parser')
		ip_list = soup.find('table', id='ip_list')
		ip_tr_list = ip_list.find_all('tr', limit=22)
		for index, ip_tr in enumerate(ip_tr_list):
			if index < 2:
				continue
			ip_td = ip_tr.find_all('td')
			address = ''
			port = ''
			for num, data in enumerate(ip_td):
				if num == 1:
					address = data.getText()
				elif num == 2:
					port = data.getText()
				elif num > 2:
					break

			ip.append(address + ':' + port)
		return ip

	@staticmethod
	def write_ip(ip_list: {}):
		for ip in ip_list:
			IP_LIST.append({"ip_port": ip})

	def run(self):
		print("reload proxy")
		content = self.get_content(URL)
		ip_list = self.parse_content(content)
		print(ip_list)
		self.write_ip(ip_list)


def task():
	crawler = ProxyCrawler()
	crawler.run()
	schedule = Scheduler()
	schedule.every().hours.do(crawler.run)
	while True:
		schedule.run_pending()
		time.sleep(1)


def start():
	thread = threading.Thread(target=task)
	thread.start()


if __name__ == '__main__':
	start()
