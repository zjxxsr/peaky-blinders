import datetime
import time
import redis
import os

rdb = redis.Redis(os.environ.get('REDIS_HOST', '127.0.0.1'), int(os.environ.get('REDIS_PORT', 6379)), 0)

fake_chat_dict = {
    0: '十全十美！',
    1: '一把钢枪交给我！',
    2: '二话不说为祖国！',
    3: '三山五岳任我走。',
    4: '四海为家。',
    5: '五福同寿。',
    6: '六六大顺！',
    7: '97香港回归。',
    8: '零八奥运。',
    9: '九九归一。',
}


def fake_chat(xinput):
    xlen = len(xinput)
    xoutput = f'您说了{xlen}个字符。（{xinput[:5]}……）' + fake_chat_dict[xlen % 10]
    return xoutput + xoutput + xoutput
    # return xoutput


def text_generation_stream(xinput):
    """
    假的推理函数
    """
    xoutput = fake_chat(xinput)
    xlen = len(xoutput)
    for i in range(xlen):
        time.sleep(0.1)
        yield xoutput[:i + 1]


print('----------------READY----------------')
while True:
    # 从redis 拿数据
    xuuid = rdb.rpop('fifo')
    if xuuid is None:
        time.sleep(0.001)  # 重要
        continue

    xinput = rdb.hget('uuid2input', xuuid)
    xusername = rdb.hget('uuid2username', xuuid)
    if xinput is None:
        time.sleep(0.001)  # 重要
        continue
    if xusername is not None:
        xusername = xusername.decode('utf8')
    xinput = xinput.decode('utf8')
    print('input:', xinput, flush=True)

    # 推理
    xgen = text_generation_stream(xinput)
    for xres in xgen:
        print(xusername, xres)
        if xusername:
            rdb.set('chat_cache_' + xusername, xres.encode('utf8'))

    # 把数据放回
    xoutput = xres
    print('output:', xoutput, flush=True)
    rdb.hset('uuid2output', xuuid, xoutput.encode('utf8'))

    time.sleep(0.001)  # 重要
