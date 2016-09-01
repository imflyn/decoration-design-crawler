from msic.core.service import mongodb_service
from tubatu.msic import constants
from msic.common import utils
from tubatu.items import RoomDesignItem
from tubatu.model.room_design import RoomDesignModel
import os
from os.path import dirname

CONFIGURE_FILE_PATH = dirname(dirname(dirname(os.path.realpath(__file__)))) + "\\scrapy.cfg"
SECTION_DATABASE = "database"
OPTION_HOST = "host"
OPTION_PORT = "prot"

DATABASE_NAME = "tubatu"
TABLE_NAME = "room_design"


class RoomDesignService(object):
	def __init__(self):
		host = utils.get_configure_content(CONFIGURE_FILE_PATH, SECTION_DATABASE, OPTION_HOST)
		port = utils.get_configure_content(CONFIGURE_FILE_PATH, SECTION_DATABASE, OPTION_PORT)
		self.client = mongodb_service.get_client(host, int(port))
		self.db = mongodb_service.get_db(self.client, DATABASE_NAME)
		self.collection = mongodb_service.get_collection(self.db, TABLE_NAME)

	def get_model(self, room_design_item: RoomDesignItem) -> RoomDesignModel:
		room_design_model = RoomDesignModel()
		room_design_model._id = utils.get_uuid()
		room_design_model.title = room_design_item['title']
		room_design_model.html_url = room_design_item['html_url']
		room_design_model.tags = room_design_item['tags']
		room_design_model.description = room_design_item['description']
		room_design_model.image_url = room_design_item['image_url']
		room_design_model.image_width = room_design_item['image_width']
		room_design_model.image_height = room_design_item['image_height']
		room_design_model.create_time = utils.get_utc_time()
		room_design_model.image_name = "/" + constants.PORJECT_NAME + "/" + room_design_model.create_time[0:10] + "/" + utils.get_md5(
			room_design_model.create_time + room_design_model.html_url)

		return room_design_model

	def saveToDatabase(self, room_design_model: RoomDesignModel):
		mongodb_service.insert(self.collection, room_design_model.__dict__)

	def __del__(self):
		self.client.close()
