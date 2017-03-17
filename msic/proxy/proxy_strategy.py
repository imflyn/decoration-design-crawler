from bs4 import BeautifulSoup

from msic.common import utils
from msic.proxy.proxy import Proxy


class GetProxyStrategy(object):
    URL = ''

    def __init__(self):
        self.content = ''

    def execute(self) -> []:
        self.content = utils.http_request(self.URL).text


class GetXiciProxyStrategy(GetProxyStrategy):
    SPEED = 100
    NAME = 'Xici'

    def execute(self):
        super(GetXiciProxyStrategy, self).execute()
        ip = []
        soup = BeautifulSoup(self.content, 'html.parser')
        ip_list = soup.find('table', id='ip_list')
        ip_tr_list = ip_list.find_all('tr', limit=101)
        for index, ip_tr in enumerate(ip_tr_list):
            if index == 0:
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
                elif num == 6 or num == 7:
                    try:
                        value = data.find('div', class_='bar').find('div').attrs['style']  # type:str
                        is_high_quality = is_high_quality and int(value.replace('width:', '').replace('%', '')) > self.SPEED
                    except:
                        break
                elif num > 7:
                    break
            if is_high_quality:
                ip.append(address + ':' + port)
        return ip


class GetXiciChinaProxyStrategy(GetXiciProxyStrategy):
    URL = 'http://www.xicidaili.com/nn/'
    SPEED = 85


class GetXiciForeignProxyStrategy(GetXiciProxyStrategy):
    URL = 'http://www.xicidaili.com/wn/'
    SPEED = 80


class Get66ipProxyStrategy(GetProxyStrategy):
    NAME = '66ip'
    URL = 'http://www.66ip.cn/nmtq.php?getnum=800&isp=0&anonymoustype=4&start=&ports=&export=&ipaddress=&area=1&proxytype=0&api=66ip'

    def execute(self):
        super(Get66ipProxyStrategy, self).execute()
        soup = BeautifulSoup(self.content, 'html.parser')
        ip = []
        for br in soup.findAll('br'):
            ip.append(br.next.strip())
        return ip


class GetKuaidailiProxyStrategy(GetProxyStrategy):
    NAME = 'Kuaidaili'
    URL = 'http://www.kuaidaili.com/proxylist/%s/'
    SPEED = 5

    def execute(self):
        ip = []
        for num in range(1, 10):
            url = self.URL % num
            context = utils.http_request(url).text
            ip = ip + self.parse(context)
        return ip

    def parse(self, content) -> []:
        ip = []
        soup = BeautifulSoup(content, 'html.parser')
        ip_table = soup.find('tbody')
        ip_tr_list = ip_table.find_all('tr')
        for ip_tr in ip_tr_list:
            ip_td = ip_tr.find_all('td')
            address = ''
            port = ''
            is_high_quality = True
            for num, data in enumerate(ip_td):
                if num == 0:
                    address = data.getText()
                elif num == 1:
                    port = data.getText()
                elif num == 2:
                    is_high_quality = data.getText() == '高匿名'
                    if not is_high_quality:
                        break
                elif num == 6:
                    try:
                        is_high_quality = is_high_quality and float(data.getText()[:-1]) < self.SPEED
                        break
                    except:
                        break
            if is_high_quality:
                ip.append(address + ':' + port)
        return ip


def crawl_proxy() -> []:
    proxy_list = []

    def get_proxy_list(_strategy):
        _proxy_list = []
        _ip_list = _strategy.execute()
        for ip in _ip_list:
            if ip.strip() == '':
                continue
            _proxy = Proxy.create(ip, _strategy.NAME)
            _proxy_list.append(_proxy)
        return _proxy_list

    # proxy_list += get_proxy_list(GetKuaidailiProxyStrategy())
    proxy_list += get_proxy_list(Get66ipProxyStrategy())
    proxy_list += get_proxy_list(GetXiciChinaProxyStrategy())
    proxy_list += get_proxy_list(GetXiciForeignProxyStrategy())
    return proxy_list
