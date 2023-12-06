import hashlib
import time
import random
from threading import Thread, Lock

def md5(xstr):
    """https://stackoverflow.com/questions/5297448/how-to-get-md5-sum-of-a-string-using-python"""
    xmd5 = hashlib.md5(xstr.encode('utf-8')).hexdigest()
    return xmd5


def uuid():
    xns = time.time_ns()
    xns = '%020d' % xns
    xrand = random.randint(0, 999999)
    xrand = '%06d' % xrand
    xuuid = xns + '_' + xrand
    return xuuid


if '__main__' == __name__:
    xin = '您好，请问今天天气如何？'
    xout = md5(xin)
    print(xin, xout)

    xin = '您好，请问顺义八维怎么走？'
    xout = md5(xin)
    print(xin, xout)

    xin = '您好，请问今天天气如何？'
    xout = md5(xin)
    print(xin, xout)

    print('Try UUID by multiple threads:')
    xlock = Lock()

    def get_and_show_uuid(i):
        xuuid = uuid()
        with xlock:
            print(i, xuuid)

    threads = []
    for i in range(10):
        th = Thread(target=get_and_show_uuid, args=(i, ))  # 建立线程
        threads.append(th)  # 把线程放入列表
        th.start()  # 运行线程

    for th in threads:  # 循环列表里的所有线程
        th.join()  # 等待线程th结束

    print('All over.')
