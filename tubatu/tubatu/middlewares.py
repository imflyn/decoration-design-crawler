import requests
from requests.adapters import HTTPAdapter

from msic.common.constant import HEADERS


class RedirectionMiddleware(object):
	def process_response(self, request, response, spider):
		if request.url == 'http://captcha.to8to.com/captcha.html':
			session = requests.Session()
			session.mount('https://', HTTPAdapter(max_retries=5))
			session.mount('http://', HTTPAdapter(max_retries=5))
			captcha_request = session.get(request.url, headers=HEADERS, timeout=30)
		# TODO get cookies
		return response

	def process_exception(self, request, exception, spider):
		pass
