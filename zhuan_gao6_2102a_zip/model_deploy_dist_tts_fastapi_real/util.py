import hashlib
import time
import random
from threading import Thread, Lock
from common import KEY
import datetime
import struct

get_pos_of_first_punct_set = set(['.', ',', '?', '!', ';', '。', '，', '？', '！', '；'])


def get_pos_of_first_punct(xstr):
    """返回第一个TTS切分标点的位置"""
    for pos, char in enumerate(xstr):
        if char in get_pos_of_first_punct_set:
            return pos
    return None


# https://docs.python.org/3/library/struct.html
# https://docs.python.org/3/library/struct.html#struct-format-strings
# > big-endian
# I unsigned int (4 byte)

WAV_HEADER_LEN = 44


def compose_wav_header(bytes_len, num_channels=1, bit_size=16, sample_rate=16000):
    assert(num_channels in [1, 2], 'num_channels must be 1 or 2!')

    header_arr = []

    header_arr.append(b'RIFF')

    header_arr.append(struct.pack('<I', bytes_len + WAV_HEADER_LEN - 8))

    header_arr.append(b'WAVE')
    header_arr.append(b'fmt ')

    header_arr.append(struct.pack('<I', 16))

    header_arr.append(struct.pack('<H', 1))

    header_arr.append(struct.pack('<H', num_channels))

    header_arr.append(struct.pack('<I', sample_rate))

    bytes_per_sec = sample_rate * bit_size * num_channels // 8
    header_arr.append(struct.pack('<I', bytes_per_sec))

    block_alignment = bit_size * num_channels // 8
    header_arr.append(struct.pack('<H', block_alignment))

    header_arr.append(struct.pack('<H', bit_size))

    header_arr.append(b'data')

    header_arr.append(struct.pack('<I', bytes_len))

    header_bytes = b''.join(header_arr)

    assert(WAV_HEADER_LEN == len(header_bytes), f'Header size must be {WAV_HEADER_LEN} bytes!')

    return header_bytes


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
