import hashlib
import time
import datetime
import random
from common import KEY
import struct


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


def merge_dialog_in_and_out(rows_in, rows_out):
    """dialog log: DESC"""
    rows = rows_in + rows_out
    rows = sorted(rows, key=lambda row: row[KEY], reverse=True)  # DESC
    return rows


def translate_ns(ns):
    ms = ns // 1000
    mili = ms // 1000
    s = mili // 1000
    ms_ = mili % 1000
    dt = datetime.datetime.fromtimestamp(s)
    xstr = dt.strftime('%Y-%m-%d %H:%M:%S')
    return '%s.%03d' % (xstr, ms_)


if '__main__' == __name__:
    print(uuid())
