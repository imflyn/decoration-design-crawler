from msic.scrapy import ip_pool

if __name__ == '__main__':
	ip_pool.IP_LIST = [
		{"ip_port": "127.0.0.1:1080"},
		{"ip_port": "127.0.0.1:1080"},
		{"ip_port": "127.0.0.1:1080"}, ]
	ip_pool.delete_ip('127.0.0.1:1080')
