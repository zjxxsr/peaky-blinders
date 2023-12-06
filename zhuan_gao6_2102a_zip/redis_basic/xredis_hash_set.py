import redis

if '__main__' == __name__:

    rdb = redis.Redis('127.0.0.1', 6379, 0)
    r = rdb.hset('hash001', 'key004', 'value004')
    print(r)
