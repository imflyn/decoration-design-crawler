import unittest

from msic.proxy.proxy_pool import ProxyPool


class TestProxyPool(unittest.TestCase):
    def setUp(self):
        self.proxy_pool = ProxyPool()

    def test_random_choice_proxy(self):
        ip = self.proxy_pool.random_choice_proxy()
        assert ip is not None
        assert not ip.strip() == ''
        print(ip)

    def test_add_failed_time(self):
        ip = self.proxy_pool.random_choice_proxy()
        # ip = '211.65.37.125:8118'
        self.proxy_pool.add_failed_time(ip)
        proxy = self.proxy_pool.collection.find_one({'ip': ip})
        print(proxy)
        print("失败次数:%s" % proxy['failed_count'])

    def test_check_ip_availability_task(self):
        self.proxy_pool.check_ip_availability_task()

    def test_crawl_proxy_task(self):
        self.proxy_pool.crawl_proxy_task()

    def test_start(self):
        self.proxy_pool.start()


if __name__ == '__main__':
    unittest.main()
