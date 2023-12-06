import redis
import time
import os

rdb = redis.Redis(os.environ.get('REDIS_HOST', '127.0.0.1'), int(os.environ.get('REDIS_PORT', 6379)), 0)

from modelscope.pipelines import pipeline
from modelscope.utils.constant import Tasks
ms_gen = pipeline(Tasks.text_generation, model='damo/nlp_gpt3_text-generation_chinese-base')
print('---------------热身运动--------------------', flush=True)
ms_gen('热身运动')


def text_generation_zh(xinput):
    xoutput = ms_gen(xinput)['text']
    xlen = len(xoutput)
    for i in range(xlen):
        time.sleep(0.15)
        yield {
            'text': xoutput[:i+1],
        }


if '__main__' == __name__:

    def _main():
        print('---------------READY--------------------', flush=True)
        while True:
            xuuid = rdb.rpop('queue')
            if xuuid is None:
                time.sleep(0.0005)  # 重要
                continue

            # 用uuid从hash得到输入
            xinput = rdb.hget('uuid2input', xuuid)
            if xinput is None:
                time.sleep(0.001)  # 重要
                continue
            xinput = xinput.decode('utf8')
            print('input:', xinput, flush=True)
            # 用uuid从hash得到username
            xusername = rdb.hget('uuid2username', xuuid)
            if xusername is None:
                time.sleep(0.001)  # 重要
                continue
            xusername = xusername.decode('utf8')
            print('username:', xusername, flush=True)

            # 输入=>输出
            xgen = text_generation_zh(xinput)
            for x in xgen:
                xoutput = x['text']
                # print('output:', xoutput)
                xoutput = xoutput.encode('utf8')
                rdb.set('chat_cache_' + xusername, xoutput)

            # 把输出放入hash
            print('output:', xoutput.decode('utf8'), flush=True)
            rdb.hset('uuid2output', xuuid, xoutput)

    _main()
