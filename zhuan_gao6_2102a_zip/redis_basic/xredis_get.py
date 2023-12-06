import redis

if '__main__' == __name__:

    rdb = redis.Redis('127.0.0.1', 6379, 0)
    r = rdb.get('keyXXX')
    r = r.decode('utf8')
    print(r)
