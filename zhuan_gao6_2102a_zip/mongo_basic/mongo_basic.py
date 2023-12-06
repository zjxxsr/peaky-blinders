from util_mongo import enqueue, get_sorted_by_key
import pymongo as pm
from common import MONGODB_NAME, VALUE, KEY, IO_PREFIX
import time

# 连接Mongodb
mongo = pm.MongoClient('127.0.0.1', 27017, serverSelectionTimeoutMS=3000)
mdb = mongo[MONGODB_NAME]

ts = time.time_ns()
enqueue(mdb, 'dialog_in', 'uxxxx', ts, '您好！')
ts = time.time_ns()
enqueue(mdb, 'dialog_in', 'uxxxx', ts, '您好！001xxxx')
ts = time.time_ns()
enqueue(mdb, 'dialog_in', 'uxxxx', ts, '您好！002yyyy')
print('Enqueue all OK')

xres = get_sorted_by_key(mdb, 'dialog_in', 'uxxxx', limit=2, is_keep_others=False)
print(xres)
print('Query all OK')
