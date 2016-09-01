import os
from os.path import dirname

CONFIGURE_FILE_PATH = dirname(dirname(dirname(os.path.realpath(__file__)))) + "\\scrapy.cfg"

print(CONFIGURE_FILE_PATH)
