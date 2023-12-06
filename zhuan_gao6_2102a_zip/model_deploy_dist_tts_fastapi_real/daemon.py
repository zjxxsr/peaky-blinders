import redis
import time
from modelscope.pipelines import pipeline
from modelscope.utils.constant import Tasks

rdb = redis.Redis('127.0.0.1', 6379, 0)
pipe = pipeline(Tasks.text_generation, model='damo/nlp_gpt3_text-generation_chinese-base')


def text_generation_zh(xinput):
    xoutput = pipe(xinput)
    return xoutput


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

    # # 看用户是否正在并行
    # r = rdb.sismember('users', xusername)
    # if r:
    #     # 用户正在并行，重新排队
    #     rdb.lpush('queue', xuuid)
    #     continue
    # else:
    #     # 用户加入集合
    #     rdb.sadd('users', xusername)

    # 输入=>输出
    rdb.set('chat_cache_' + xusername, '正在生成……')
    xoutput = text_generation_zh(xinput)
    xoutput = xoutput['text']

    # 把输出放入hash
    rdb.hset('uuid2output', xuuid, xoutput)

    # 用户移出集合
    rdb.srem('users', xusername)
