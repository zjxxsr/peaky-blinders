import redis

if '__main__' == __name__:

    rdb = redis.Redis('127.0.0.1', 6379, 0)

    r = rdb.sadd('set002', 'aaa')
    print(r)
    r = rdb.sadd('set002', 'bbb')
    print(r)
    r = rdb.sadd('set002', 'ccc')
    print(r)
    r = rdb.sadd('set002', 'ddd')
    print(r)

    r = rdb.smembers('set002')
    print(r)

    r = rdb.sismember('set002', 'bbb')
    print(r)
    r = rdb.sismember('set002', 'bbbb')
    print(r)

    r = rdb.srem('set002', 'bbb')
    print(r)

    r = rdb.smembers('set002')
    print(r)
