import redis

if '__main__' == __name__:

    rdb = redis.Redis('127.0.0.1', 6379, 0)
    r = rdb.smembers('set001')
    print(r)
    r = rdb.sismember('set001', 'a')
    print(r)
    r = rdb.sismember('set001', 'aaa')
    print(r)
