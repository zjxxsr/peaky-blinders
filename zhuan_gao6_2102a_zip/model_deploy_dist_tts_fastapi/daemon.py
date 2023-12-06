import redis
import time

rdb = redis.Redis('127.0.0.1', 6379, 0)

fake_chat_dict = {
    0: '十全十美！',
    1: '一把钢枪交给我！',
    2: '二话不说为祖国！',
    3: '三山五岳任我走。',
    4: '四海为家',
    5: '五福同寿',
    6: '六六大顺！',
    7: '97香港回归。',
    8: '零八奥运。',
    9: '九九归一。',
}


def text_generation_zh(xinput):
    xlen = len(xinput)
    xoutput = f'您说了{xlen}个字符。（{xinput[:10]}……）'
    for i in range(10):
        xoutput += fake_chat_dict[(i + xlen) % 10]
    xoutput = xoutput + xoutput + xoutput + xoutput
    xlen = len(xoutput)
    for i in range(xlen):
        time.sleep(0.0001)
        yield {
            'text': xoutput[:i+1],
        }


print('---------------READY--------------------')
while True:
    xuuid = rdb.rpop('queue')
    if xuuid is None:
        time.sleep(0.001)  # 重要
        continue

    # 用uuid从hash得到输入
    xinput = rdb.hget('uuid2input', xuuid)
    if xinput is None:
        time.sleep(0.001)  # 重要
        continue
    xinput = xinput.decode('utf8')
    print('input:', xinput)
    # 用uuid从hash得到username
    xusername = rdb.hget('uuid2username', xuuid)
    if xusername is None:
        time.sleep(0.001)  # 重要
        continue
    xusername = xusername.decode('utf8')
    print('username:', xusername)

    # 看用户是否正在并行
    r = rdb.sismember('users', xusername)
    if r:
        # 用户正在并行，重新排队
        rdb.lpush('queue', xuuid)
        continue
    else:
        # 用户加入集合
        rdb.sadd('users', xusername)

    # 输入=>输出
    xgen = text_generation_zh(xinput)
    for x in xgen:
        xoutput = x['text']
        # print('output:', xoutput)
        xoutput = xoutput.encode('utf8')
        rdb.set('chat_cache_' + xusername, xoutput)

    # 把输出放入hash
    rdb.hset('uuid2output', xuuid, xoutput)

    # 用户移出集合
    rdb.srem('users', xusername)
