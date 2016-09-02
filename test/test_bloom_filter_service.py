from msic.core.service.bloom_filter_service import RedisBloomFilter

if __name__ == '__main__':
	uid = ['alskdjflkasjdf', 'kajdsklfjlkasdf', 'lhjkkjhrwqer', 'alskdjflkasjdf']
	bf = RedisBloomFilter()
	err_time = 0
	for index, id in enumerate(uid):
		if bf.is_contains(id, 'test'):
			err_time += 1
		else:
			bf.insert(id, 'test')
	print(err_time)
