import unittest

import requests
from requests.adapters import HTTPAdapter

from msic.common.constant import HEADERS


class TestRequests(unittest.TestCase):
	def setUp(self):
		pass

	def test_captcha(self):
		session = requests.Session()
		session.mount('https://', HTTPAdapter(max_retries=5))
		session.mount('http://', HTTPAdapter(max_retries=5))
		response = session.get('http://captcha.to8to.com/captcha.html', headers=HEADERS, timeout=30)
		print(session.cookies.get_dict())


if __name__ == '__main__':
	unittest.main()
