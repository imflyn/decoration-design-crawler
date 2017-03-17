import requests
from PIL import Image
from tubatu.constants import PROJECT_NAME

from msic.common import utils
from msic.proxy.proxy_pool import proxy_pool
from tubatu import config

IMAGE_SIZE = 500, 500


class ImageService(object):
    @staticmethod
    def generate_name(key):
        create_time = utils.get_utc_time()
        img_name = "/" + PROJECT_NAME + "/" + create_time[0:10] + "/" + utils.get_md5(create_time + key)
        return img_name

    @staticmethod
    def get_file_name(image_name) -> str:
        name_data = image_name[1:].split("/")
        project_name = name_data[0]
        date = name_data[1]
        file_name = name_data[2]
        return "/" + project_name + "/" + date + "/" + file_name

    @staticmethod
    def file_path(image_name):
        file_path = ImageService.get_file_name(image_name)
        dir_name = file_path[0:file_path.rfind("/")]
        utils.make_dirs(config.IMAGES_STORE + dir_name)
        path = config.IMAGES_STORE + '%s_original.jpg' % file_path
        return path

    @staticmethod
    def thumb_path(image_name):
        file_path = ImageService.get_file_name(image_name)
        dir_name = file_path[0:file_path.rfind("/")]
        utils.make_dirs(config.IMAGES_STORE + dir_name)
        path = config.IMAGES_STORE + '%s_thumb.jpg' % file_path
        return path

    @staticmethod
    def download_img(img_url, file_path):
        proxies = None
        proxy = ''
        if config.USE_PROXY:
            proxy = proxy_pool.random_choice_proxy()
            proxies = {
                'http': "http://%s" % proxy,
            }
        try:
            response = requests.get(img_url, stream=True, proxies=proxies)
            if response.status_code == 200:
                with open(file_path, 'wb') as f:
                    for chunk in response.iter_content(1024):
                        f.write(chunk)
            else:
                if config.USE_PROXY:
                    proxy_pool.add_failed_time(proxy)
        except:
            if config.USE_PROXY:
                proxy_pool.add_failed_time(proxy)

    @staticmethod
    def save_thumbnail(file_path, thumb_path):
        image = Image.open(file_path)
        if thumb_path is not None:
            image.thumbnail(IMAGE_SIZE)
            image.save(thumb_path)
        del image
