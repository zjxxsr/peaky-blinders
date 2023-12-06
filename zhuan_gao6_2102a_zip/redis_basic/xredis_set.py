import redis

if '__main__' == __name__:

    rdb = redis.Redis('127.0.0.1', 6379, 0)
    r = rdb.set('keyXXX', '外文文本XXX'.encode('utf8'))
    print(r)
