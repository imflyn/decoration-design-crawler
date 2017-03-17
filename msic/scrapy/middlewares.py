import random

from scrapy.http import HtmlResponse
from selenium import webdriver
from selenium.webdriver import DesiredCapabilities

from msic.common import log, agents
from msic.proxy.proxy_pool import proxy_pool

JAVASCRIPT = 'JAVASCRIPT'


class CatchExceptionMiddleware(object):
    def process_response(self, request, response, spider):
        if response.status < 200 or response.status >= 400:
            try:
                proxy_pool.add_failed_time(request.meta['proxy'].replace('http://', ''))
            except KeyError:
                pass
        return response

    def process_exception(self, request, exception, spider):
        try:
            proxy_pool.add_failed_time(request.meta['proxy'].replace('http://', ''))
        except Exception:
            pass


class CustomHttpProxyMiddleware(object):
    def process_request(self, request, spider):
        try:
            request.meta['proxy'] = "http://%s" % proxy_pool.random_choice_proxy()
        except Exception as e:
            log.error(e)


class CustomUserAgentMiddleware(object):
    def process_request(self, request, spider):
        agent = random.choice(agents.AGENTS_ALL)
        request.headers['User-Agent'] = agent


class JavaScriptMiddleware(object):
    def process_request(self, request, spider):
        if JAVASCRIPT in request.meta and request.meta[JAVASCRIPT] is True:
            driver = self.phantomjs_opened()
            try:
                driver.get(request.url)
                body = driver.page_source
                return HtmlResponse(request.url, body=body, encoding='utf-8', request=request)
            finally:
                self.phantomjs_closed(driver)

    def phantomjs_opened(self):
        capabilities = DesiredCapabilities.PHANTOMJS.copy()
        proxy = proxy_pool.random_choice_proxy()
        capabilities['proxy'] = {
            'proxyType': 'MANUAL',
            'ftpProxy': proxy,
            'sslProxy': proxy,
            'httpProxy': proxy,
            'noProxy': None
        }
        # capabilities['phantomjs.cli.args'] = [
        # 	'--proxy-auth=' + evar.get('WONDERPROXY_USER') + ':' + evar.get('WONDERPROXY_PASS')
        # ]
        driver = webdriver.PhantomJS(desired_capabilities=capabilities)
        driver.set_page_load_timeout(120)
        return driver

    def phantomjs_closed(self, driver):
        driver.quit()
