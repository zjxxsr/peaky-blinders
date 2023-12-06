import redis

if '__main__' == __name__:

    rdb = redis.Redis('127.0.0.1', 6379, 0)
    for i in range(4):
        r = rdb.set(f'key00{i}', f'文本00{i}'.encode('utf-8'))
        print('result:', r)
