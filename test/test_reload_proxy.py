from msic.scrapy.reload_proxy import ProxyCrawler
from msic.scrapy.reload_proxy import IP_LIST
from msic.scrapy import reload_proxy

if __name__ == '__main__':
	# proxy_crawler = ProxyCrawler()
	# proxy_crawler.write_ip({'119.188.94.145', '1.25.201.12', '218.244.149.184'})
	# print(IP_LIST)
	# proxy_crawler.write_ip({'120.25.105.45', '123.56.218.131', '118.165.114.130'})
	# print(IP_LIST)

	reload_proxy.start('http://www.163.com')
