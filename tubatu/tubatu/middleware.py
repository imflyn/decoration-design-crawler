import random
from msic import agents, log, proxy


class CustomHttpProxyMiddleware(object):
	def process_request(self, request, spider):
		# TODO implement complex proxy providing algorithm
		if self.use_proxy(request):
			p = random.choice(proxy.FREE_PROXIES)
			try:
				request.meta['proxy'] = "http://%s" % p['ip_port']
			except Exception as e:
				log.error("Exception %s" % e)

	def use_proxy(self, request):
		"""
		using direct download for depth <= 2
		using proxy with probability 0.3
		"""
		if "depth" in request.meta and int(request.meta['depth']) <= 2:
			return False
		i = random.randint(1, 10)
		return i <= 2


class CustomUserAgentMiddleware(object):
	def process_request(self, request, spider):
		agent = random.choice(agents)
		request.headers['User-Agent'] = agent
