from redis import StrictRedis


class SimpleHash(object):
    def __init__(self, cap, seed):
        self.cap = cap
        self.seed = seed

    def hash(self, value):
        ret = 0
        for i in range(value.__len__()):
            ret += self.seed * ret + ord(value[i])
        return (self.cap - 1) & ret


class RedisBloomFilter(object):
    def __init__(self, redis_client: StrictRedis):
        self.bit_size = 1 << 25
        self.seeds = [5, 7, 11, 13, 31, 37, 61]
        self.redis = redis_client
        self.hash_dict = []
        for i in range(self.seeds.__len__()):
            self.hash_dict.append(SimpleHash(self.bit_size, self.seeds[i]))

    def is_contains(self, value, key):
        if value is None:
            return False
        if value.__len__() == 0:
            return False
        ret = True
        for f in self.hash_dict:
            loc = f.hash(value)
            ret = ret & self.redis.getbit(key, loc)
        return ret

    def insert(self, value, key):
        for f in self.hash_dict:
            loc = f.hash(value)
            self.redis.setbit(key, loc, 1)
