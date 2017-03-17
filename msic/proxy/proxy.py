from msic.common import utils


class Proxy(object):
    def __init__(self):
        self.ip = ''
        self.response_speed = -1
        self.validity = False
        self.origin = ''
        self.create_time = ''
        self.update_time = ''
        self.failed_count = 0

    @staticmethod
    def create(ip, origin):
        proxy = Proxy()
        proxy.ip = ip
        proxy.origin = origin
        proxy.create_time = utils.get_utc_time()
        proxy.update_time = proxy.create_time
        proxy.failed_count = 0
        proxy.response_speed = -1
        proxy.validity = False
        return proxy
