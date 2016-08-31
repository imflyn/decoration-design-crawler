import uuid
import datetime
import time
import hashlib


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


if __name__ == '__main__':
	print("uuid:" + get_uuid())
	print("utc time:" + get_utc_time())
	print("md5:" + get_md5(get_uuid()))
