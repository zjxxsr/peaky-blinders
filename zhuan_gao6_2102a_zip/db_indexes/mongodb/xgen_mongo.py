from util_mongo import enqueue, get_sorted_by_key
import pymongo as pm
from common import MONGODB_NAME

if '__main__' == __name__:

    # 连接Mongodb
    mongo = pm.MongoClient('127.0.0.1', 27017, serverSelectionTimeoutMS=3000)
    mdb = mongo[MONGODB_NAME]

    N_UNIT = 1000
    N_USERS = 20
    for i in range(333, 380): # next 329
        print(i)
        for j in range(N_UNIT):
            xorder = i * N_UNIT + j
            xorder_user = xorder % N_USERS
            xvalue = f'第{xorder}条数据'
            xuser = f'u{xorder_user:03d}'
            enqueue(mdb, 'test_table001', xuser, xorder, xvalue)
    print('Data generation done.')
