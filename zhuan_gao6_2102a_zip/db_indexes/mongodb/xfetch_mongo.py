from util_mongo import enqueue, get_sorted_by_key
import pymongo as pm
import datetime
from common import MONGODB_NAME

if '__main__' == __name__:

    # 连接Mongodb
    mongo = pm.MongoClient('127.0.0.1', 27017, serverSelectionTimeoutMS=3000)
    mdb = mongo[MONGODB_NAME]

    dt1 = datetime.datetime.now()
    print(dt1)

    xrows = get_sorted_by_key(mdb, 'test_table001', 'u019', limit=10)
    print(xrows)

    dt2 = datetime.datetime.now()
    print(dt2)
    xdelta = dt2 - dt1
    print(xdelta)

    # index:    0:00:00.004000
    # index:    0:00:00.005000
    # index:    0:00:00.004000
    # no-index: 0:00:00.236001
    # no-index: 0:00:00.246999
    # no-index: 0:00:00.282617
