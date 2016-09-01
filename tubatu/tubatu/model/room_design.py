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
		self.image_name = ""

	# def __iter__(self):
	# 	yield '_id', self._id
	# 	yield 'title', self.title
	# 	yield 'html_url', self.html_url
	# 	yield 'tags', self.tags
	# 	yield 'description', self.description
	# 	yield 'image_url', self.image_url
	# 	yield 'image_width', self.image_width
	# 	yield 'image_height', self.image_height
	# 	yield 'image_file_path', self.image_file_path
	# 	yield 'create_time', self.create_time
	# 	yield 'image_name', self.image_name


if __name__ == '__main__':
	roomdesignmodel = RoomDesignModel()
	print(roomdesignmodel.__dict__)
