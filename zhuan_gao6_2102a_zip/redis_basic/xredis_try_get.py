import redis

if '__main__' == __name__:

    rdb = redis.Redis('127.0.0.1', 6379, 0)
    for i in range(4):
        key = f'key00{i}'
        print(key)
        value = rdb.get(key)
        print(value)
        if value is not None:
            value = value.decode('utf-8')
            print(value)
