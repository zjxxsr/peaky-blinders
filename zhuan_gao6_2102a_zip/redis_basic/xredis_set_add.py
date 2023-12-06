import redis

if '__main__' == __name__:

    rdb = redis.Redis('127.0.0.1', 6379, 0)
    r = rdb.sadd('set001', 'd')
    print(r)
    r = rdb.sadd('set001', 'e')
    print(r)
    r = rdb.sadd('set001', 'f')
    print(r)
