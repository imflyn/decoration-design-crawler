import datetime
import hashlib
import os
import uuid

import requests
from requests import Response
from requests.adapters import HTTPAdapter

from msic.common.constant import HEADERS


# 2a47d8b6-6f5b-11e6-ac9d-64006a0b51ab
def get_uuid() -> str:
    return str(uuid.uuid1())


# 2016-08-31T09:13:22.434Z
def get_utc_time() -> str:
    return datetime.datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%S.%f")[:-3] + "Z"


def get_md5(content: str) -> str:
    md5 = hashlib.md5()
    md5.update(content.encode('utf-8'))
    return md5.hexdigest()


def make_dirs(path: str):
    if not os.path.exists(path):
        os.makedirs(path, exist_ok=True)


def http_request(url: str, timeout=30) -> Response:
    session = requests.Session()
    session.mount('https://', HTTPAdapter(max_retries=5))
    session.mount('http://', HTTPAdapter(max_retries=5))
    response = session.get(url, headers=HEADERS, timeout=timeout)
    return response


def log(content: str):
    print("============================= {content} ==========================".format(content=(get_utc_time() + " " + content)))
