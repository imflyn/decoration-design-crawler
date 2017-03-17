# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

from tubatu.service.design_picture_service import DesignPictureService
from tubatu.service.design_topic_service import DesignTopicService
from tubatu.service.image_service import ImageService


class DesignPicturePipeline(object):
    def __init__(self):
        self.design_picture_service = DesignPictureService()

    def process_item(self, item, spider):
        img_url = item['img_url']
        img_name = ImageService.generate_name(img_url)
        file_path = ImageService.file_path(img_name)
        thumb_path = ImageService.thumb_path(img_name)
        ImageService.download_img(img_url, file_path)
        ImageService.save_thumbnail(file_path, thumb_path)
        item['img_name'] = img_name
        self.design_picture_service.handle_item(item)


class DesignTopicPipeline(object):
    def __init__(self):
        self.design_topic_service = DesignTopicService()

    def process_item(self, item, spider):
        article = item['article']
        for part in article:
            img_url = part['img_url']
            img_name = ImageService.generate_name(img_url)
            file_path = ImageService.file_path(img_name)
            thumb_path = ImageService.thumb_path(img_name)
            ImageService.download_img(img_url, file_path)
            ImageService.save_thumbnail(file_path, thumb_path)
            part['img_name'] = img_name
        self.design_topic_service.handle_item(item)
