from tubatu.msic import constants
from msic.common import utils
from tubatu.items import RoomDesignItem
from tubatu.model.room_design import RoomDesignModel


class RoomDesignService(object):
	def __init__(self):
		pass

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
		room_design_model.image_name = "/" + constants.PORJECT_NAME + "/" + room_design_model.create_time[0:9] + "/" + utils.get_md5(
			room_design_model.create_time + room_design_model.html_url)
