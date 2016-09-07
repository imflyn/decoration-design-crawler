class RoomDesignModel(object):
	def __init__(self):
		self._id = ""
		self.title = ""
		self.html_url = ""
		self.tags = {}
		self.description = ""
		self.image_url = ""
		self.image_width = 0
		self.image_height = 0
		self.image_file_path = ""
		self.create_time = 0
		self.image_name = ""  # /tubatu/2016-09-01/ff5e6d6e5abafbaeb56af2b5034d83e9


if __name__ == '__main__':
	roomdesignmodel = RoomDesignModel()
	print(roomdesignmodel.__dict__)
