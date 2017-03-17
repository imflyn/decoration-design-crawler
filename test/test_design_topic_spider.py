import os
import sys
import unittest
from os.path import dirname

import requests
from scrapy import Selector
from scrapy.http import Response

from tubatu.tubatu.items import DesignTopicItem

path = dirname(os.path.abspath(os.path.dirname(__file__)))
sys.path.append(path)


class TestDesignTopicSpider(unittest.TestCase):
    def test_parse_content(self):
        content = requests.get('http://xiaoguotu.to8to.com/topic/11.html')
        response = Response('http://xiaoguotu.to8to.com/topic/11.html')
        response.text = content.content.decode("utf-8")
        selector = Selector(response)
        title = selector.xpath('//div[@class="xdb_title"]/h1/text()').extract()[0]
        description = selector.xpath('//div[@class="xdbc_description"]//div//p/text()').extract()[0]
        items_selector = selector.xpath('//div[@class="xdbc_main_content"]//p')
        article = []
        text = ''
        for index, item_selector in enumerate(items_selector):
            try:
                text = item_selector.xpath('span/text()').extract()[0]
            except IndexError:
                try:
                    img_url = item_selector.xpath('img/@src').extract()[0]
                    img_width = 0
                    try:
                        img_width = item_selector.xpath('img/@width').extract()[0]
                    except IndexError:
                        pass
                    img_height = 0
                    try:
                        img_height = item_selector.xpath('img/@height').extract()[0]
                    except IndexError:
                        pass
                    article.append({'content': text, 'img_url': img_url, 'img_width': img_width, 'img_height': img_height})
                except IndexError:
                    continue
        design_topic_item = DesignTopicItem()
        design_topic_item['title'] = title
        design_topic_item['description'] = description
        design_topic_item['article'] = article
        design_topic_item['html_url'] = response.url
        return design_topic_item


if __name__ == '__main__':
    unittest.main()
