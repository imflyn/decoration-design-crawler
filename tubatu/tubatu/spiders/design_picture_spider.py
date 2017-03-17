import json

import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.selector import Selector
from scrapy.spiders import CrawlSpider
from scrapy.spiders import Rule
from tubatu.constants import ZONE_TYPE, STYLE_ID, AREA, COLOR_ID, HX_ID, PART_ID
from tubatu.items import DesignPictureItem
from tubatu.service.design_picture_service import DesignPictureService

from msic.common import log, constant
from msic.common import utils
from msic.proxy.proxy_pool import proxy_pool
from tubatu import config


class DesignPictureSpider(CrawlSpider):
    start_url_domain = 'xiaoguotu.to8to.com'
    name = 'design_picture'
    allowed_domains = ['to8to.com']
    start_urls = ['http://xiaoguotu.to8to.com/tuce/']
    rules = (
        Rule(LinkExtractor(allow="/tuce/p_\d+.html"), follow=True, callback='parse_list'),
    )
    custom_settings = {
        'ITEM_PIPELINES': {
            'tubatu.pipelines.DesignPicturePipeline': 302,
        }
    }
    design_picture_service = DesignPictureService()

    def parse_list(self, response):
        selector = Selector(response)
        items_selector = selector.xpath('//div[@class="xmp_container"]//div[@class="item"]')
        for item_selector in items_selector:
            # http://xiaoguotu.to8to.com/c10037052.html
            cid = item_selector.xpath('div//a/@href').extract()[0][2:-6]
            title = item_selector.xpath('div//a/@title').extract()[0]
            # http://xiaoguotu.to8to.com/getxgtjson.php?a2=0&a12=&a11=10037052&a1=0
            next_url = (constant.PROTOCOL_HTTP + self.start_url_domain + '/getxgtjson.php?a2=0&a12=&a11={cid}&a1=0').format(cid=cid)
            yield scrapy.Request(next_url, self.parse_content, meta={'cid': cid, 'title': title})

    def parse_content(self, response):
        uuid = utils.get_uuid()
        cid = response.meta['cid']
        title = response.meta['title']
        try:
            data = json.loads(response.text)
        except:
            print("-----------------------获取到json:" + response.text + "------------------------------")
            return
        data_img_list = data['dataImg']
        data_album_list = None
        for _data_img in data_img_list:
            if _data_img['cid'] == cid:
                data_album_list = _data_img['album']
                break
        for data_album in data_album_list:
            data_img = data_album['l']
            # http://pic.to8to.com/case/1605/05/20160505_f0af86a239d0b02e9635a47ih5l1riuq_sp.jpg
            img_url = 'http://pic.to8to.com/case/{short_name}'.format(short_name=data_img['s'])
            if self.design_picture_service.is_duplicate_url(img_url):
                break
            sub_title = data_img['t']
            original_width = data_img['w']
            original_height = data_img['h']
            tags = []
            try:
                zoom_type = ZONE_TYPE[data_img['zid']]
                if zoom_type is not None or not zoom_type.strip() == '':
                    tags.append(zoom_type)
            except KeyError:
                pass
            try:
                style_id = STYLE_ID[data_img['sid']]
                if style_id is not None or not style_id.strip() == '':
                    tags.append(style_id)
            except KeyError:
                pass
            try:
                area = AREA[data_img['a']]
                if area is not None or not area.strip() == '':
                    tags.append(area)
            except KeyError:
                pass
            try:
                color_id = COLOR_ID[data_img['coid']]
                if color_id is not None or not color_id.strip() == '':
                    tags.append(color_id)
            except KeyError:
                pass
            try:
                house_type = HX_ID[data_img['hxid']]
                if house_type is not None or not house_type.strip() == '':
                    tags.append(house_type)
            except KeyError:
                pass
            try:
                part = PART_ID[data_img['pid']]
                if part is not None or not part.strip() == '':
                    tags.append(part)
            except KeyError:
                pass
            try:
                design_picture_item = DesignPictureItem()  # type: DesignPictureItem
                design_picture_item['fid'] = uuid
                design_picture_item['html_url'] = response.url
                design_picture_item['img_url'] = img_url
                design_picture_item['tags'] = tags
                design_picture_item['title'] = title
                design_picture_item['sub_title'] = sub_title
                design_picture_item['img_width'] = original_width
                design_picture_item['img_height'] = original_height
                design_picture_item['description'] = design_picture_item['title']
                yield design_picture_item
            except Exception as e:
                print("-----------------------获取到json:" + response.text + "------------------------------")
                log.warn("%s ( refer: %s )" % (e, response.url))
                if config.USE_PROXY:
                    proxy_pool.add_failed_time(response.meta['proxy'].replace('http://', ''))
