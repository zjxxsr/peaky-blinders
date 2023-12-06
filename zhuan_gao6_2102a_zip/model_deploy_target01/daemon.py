import redis
import time

rdb = redis.Redis('127.0.0.1', 6379, 0)

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


def text_generation_zh(xinput):
    xlen = len(xinput)
    xoutput = f'您说了{xlen}个字符。（{xinput[:5]}……）' + fake_chat_dict[xlen % 10]
    time.sleep(1.0)
    return {
        'text': xoutput,
    }

print('---------------READY--------------------')
while True:
    xuuid = rdb.rpop('queue')
    if xuuid is None:
        time.sleep(0.001)  # 重要
        continue

    # 用md5从hash得到输入
    xinput = rdb.hget('uuid2input', xuuid)
    if xinput is None:
        time.sleep(0.001)  # 重要
        continue
    xinput = xinput.decode('utf8')
    print('input:', xinput)

    # 输入=>输出
    xoutput = text_generation_zh(xinput)
    xoutput = xoutput['text']
    print('output:', xoutput)
    xoutput = xoutput.encode('utf8')

    # 把输出放入hash
    rdb.hset('uuid2output', xuuid, xoutput)
