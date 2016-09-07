import sys
import os
from os.path import dirname

path = dirname(os.path.abspath(os.path.dirname(__file__)))
sys.path.append(path)

from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings

from msic.scrapy import ip_pool
from tubatu.spiders.room_spider import RoomSpider

# "http://xiaoguotu.to8to.com/robots.txt"
ip_pool.start('http://www.baidu.com')

# runner = CrawlerRunner(get_project_settings())
#
# d = runner.crawl('room')
# d.addBoth(lambda _: reactor.stop())
# reactor.run()


process = CrawlerProcess(get_project_settings())
process.crawl(RoomSpider())
process.start()
