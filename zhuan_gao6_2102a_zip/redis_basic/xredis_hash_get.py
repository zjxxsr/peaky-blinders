import redis

if '__main__' == __name__:

    rdb = redis.Redis('127.0.0.1', 6379, 0)
    r = rdb.hget('hash001', 'key003')
    print(r)