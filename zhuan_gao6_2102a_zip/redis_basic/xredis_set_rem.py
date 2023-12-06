import redis

if '__main__' == __name__:

    rdb = redis.Redis('127.0.0.1', 6379, 0)
    r = rdb.smembers('set001')
    print(r)
    r = rdb.srem('set001', 'd')
    print(r)
    r = rdb.smembers('set001')
    print(r)
