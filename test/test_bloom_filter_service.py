import redis

from msic.core.service.bloom_filter_service import RedisBloomFilter

REDIS_HOST = '127.0.0.1'
REDIS_PORT = 6379

REDIS_DATABASE_NAME = 0

redis_client = redis.StrictRedis(host=REDIS_HOST, port=REDIS_PORT, db=REDIS_DATABASE_NAME)

if __name__ == '__main__':
    bf = RedisBloomFilter(redis_client)
    print(bf.is_contains('http://xiaoguotu.to8to.com/p10482698.html', "room_design"))
