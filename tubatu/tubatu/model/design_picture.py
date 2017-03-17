class DesignPictureModel(object):
    def __init__(self):
        self.id = ""
        self.fid = ""
        self.title = ""
        self.sub_title = ""
        self.html_url = ""
        self.tags = []
        self.description = ""
        self.img_url = ""
        self.img_width = 0
        self.img_height = 0
        self.img_name = ""  # /tubatu/2016-09-01/ff5e6d6e5abafbaeb56af2b5034d83e9
        self.create_time = ""


class DesignPictureSummaryModel(object):
    def __init__(self):
        self.id = ""
        self.cid = []
        self.title = ""
        self.description = ""
        self.tags = []
        self.html_url = ""
        self.create_time = ""
        self.update_time = ""
        self.cover_img_url = ""
        self.cover_img_width = 0
        self.cover_img_height = 0
        self.cover_img_name = ""
