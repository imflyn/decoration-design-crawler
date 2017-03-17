import json

import scrapy
from guju.items import DesignStrategyItem
from guju.service.design_strategy_service import DesignStrategyService
from scrapy.linkextractors import LinkExtractor
from scrapy.selector import Selector
from scrapy.spiders import CrawlSpider
from scrapy.spiders import Rule

from guju import config
from msic.common import constant
from msic.common import log
from msic.proxy.proxy_pool import proxy_pool


class DesignStrategySpider(CrawlSpider):
    start_url_domain = 'guju.com.cn'
    name = 'design_strategy'
    allowed_domains = ['guju.com.cn']
    start_urls = ['http://guju.com.cn/strategy/new']
    rules = (
        Rule(LinkExtractor(allow="/strategy/new/p-\d+"), follow=True, callback='parse_list'),
    )
    custom_settings = {
        'ITEM_PIPELINES': {
            'guju.pipelines.DesignStrategyPipeline': 302,
        }
    }
    design_strategy_service = DesignStrategyService()

    def parse_list(self, response):
        selector = Selector(response)
        items_selector = selector.xpath('//div[@id="listITme"]//div[@class="gl-listItem"]')
        for item_selector in items_selector:
            id = item_selector.xpath('a/@href').extract()[0].replace('/strategy/', '')
            # http://guju.com.cn/strategy/strategy_getStrategyInfo_ajax?strategyModel.id=4498
            next_url = (constant.PROTOCOL_HTTP + self.start_url_domain + '/strategy/strategy_getStrategyInfo_ajax?strategyModel.id={id}').format(
                id=id)
            if self.design_strategy_service.is_duplicate_url(next_url):
                log.info("=================过滤了" + next_url + "===========")
                continue
            yield scrapy.Request(next_url, self.parse_content, meta={'id': id})

    def parse_content(self, response):
        try:
            data = json.loads(response.text)
        except:
            print("-----------------------获取到json:" + response.text + "------------------------------")
            return
        try:
            model = data['strategyModel']
            category = model['categoryName']
            title = model['title']
            description = model['description']
            content = model['context']

            design_strategy_item = DesignStrategyItem()  # type: DesignStrategyItem
            design_strategy_item['category'] = category
            design_strategy_item['title'] = title
            design_strategy_item['description'] = description
            design_strategy_item['content'] = content
            design_strategy_item['html_url'] = response.url
            yield design_strategy_item
        except Exception as e:
            print("-----------------------获取到json:" + response.text + "------------------------------")
            log.warn("%s ( refer: %s )" % (e, response.url))
            if config.USE_PROXY:
                proxy_pool.add_failed_time(response.meta['proxy'].replace('http://', ''))
