import redis
import time
from transformers import AutoTokenizer, AutoModel
from util_mongo import get_sorted_by_key
from util import merge_dialog_in_and_out
import pymongo as pm
from common import MONGODB_NAME, VALUE, KEY, IO_PREFIX, IO_TBLS, RATE, CHAT_HISTORY_LIMIT, MAX_TOKEN

# 连接redis
rdb = redis.Redis('127.0.0.1', 6379, 0)

# 连接Mongodb
mongo = pm.MongoClient('127.0.0.1', 27017, serverSelectionTimeoutMS=3000)
mdb = mongo[MONGODB_NAME]

xpath = '/root/autodl-tmp/chatglm2-6b'
tokenizer = AutoTokenizer.from_pretrained(xpath, trust_remote_code=True)
model = AutoModel.from_pretrained(xpath, trust_remote_code=True, device='cuda')
model = model.eval()


def text_generation_zh(xinput, history=[]):
    xres = model.stream_chat(tokenizer, xinput, history=history)
    return xres


def get_history(username, base_token=0):
    rows_in = get_sorted_by_key(mdb, 'dialog_in', username, limit=CHAT_HISTORY_LIMIT, is_keep_others=False)
    rows_out = get_sorted_by_key(mdb, 'dialog_out', username, limit=CHAT_HISTORY_LIMIT, is_keep_others=False)
    rows = merge_dialog_in_and_out(rows_in, rows_out)  # 倒序

    if not len(rows):
        log = []
    else:
        # 按倒序构建聊天历史
        n_tokens = base_token
        log = []
        pair = [None, None]
        xnow_i = 0
        xnow_o = 0
        for row in rows:
            xstr = row[VALUE]
            xkey = row[KEY]
            
            # 如果聊天历史超出Encoder最多Token数量，则停止构建，并把超出范围的历史删除
            n_token_this = len(tokenizer.encode(xstr))
            n_tokens += n_token_this
            if n_tokens > MAX_TOKEN:
                delete_many_by_user(mdb, 'dialog_in', username, {
                    KEY: {
                        '$lte': xkey,
                    }
                })
                delete_many_by_user(mdb, 'dialog_out', username, {
                    KEY: {
                        '$lte': xkey,
                    }
                })
                break

            if 'i' == row['io']:
                if pair[0] is not None:
                    log.append(pair)
                    pair = [xstr, None]
                    xnow_i = xkey
                    continue
                pair[0] = xstr
                xnow_i = xkey
            elif 'o' == row['io']:
                if pair[1] is not None or xkey < xnow_i:
                    log.append(pair)
                    pair = [None, xstr]
                    xnow_o = xkey
                    continue
                pair[1] = xstr
                xnow_o = xkey
            
        log.append(pair)
        
        log = log[::-1]  # 倒序变正序

    return log


if '__main__' == __name__:

    def _main():
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

            # 从mongo拿聊天历史
            n_base_token = len(tokenizer.encode(xinput))
            xhis = get_history(xusername, n_base_token)
            for i, xh in enumerate(xhis):
                print(i, xh[0], '>>>>', xh[1])

            # 输入=>输出
            xgen = text_generation_zh(xinput, xhis)
            for x, _ in xgen:
                xoutput = x
                # print('output:', xoutput)
                xoutput = xoutput.encode('utf8')
                rdb.set('chat_cache_' + xusername, xoutput)

            # 把输出放入hash
            rdb.hset('uuid2output', xuuid, xoutput)

    _main()
