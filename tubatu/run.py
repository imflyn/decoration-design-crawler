from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings

from msic.scrapy import reload_proxy
from tubatu.spiders.room_spider import RoomSpider

reload_proxy.start()

# runner = CrawlerRunner(get_project_settings())
#
# d = runner.crawl('room')
# d.addBoth(lambda _: reactor.stop())
# reactor.run()

process = CrawlerProcess(get_project_settings())
process.crawl(RoomSpider())
process.start()
