from flask import Flask, url_for, request
from util import md5, uuid
import redis
import time

app = Flask(__name__)
rdb = redis.Redis('127.0.0.1', 6379, 0)
PWD = 'my_password_001'


@app.route("/api", methods=['POST'])
def do_infer():
    # 接收输入
    req_json = request.get_json(force=True)  # 请求json
    xinput = req_json['input']
    xusername = req_json['username']

    # 防止蹭模型
    xcheck = req_json['check']
    xmy_check = md5(xinput + PWD + xusername)
    if xcheck.lower() != xmy_check.lower():
        print('Checking not passed!')
        return None

    print('input:', xinput)

    # 数据放入队列和hash
    xuuid = uuid()
    rdb.lpush('queue', xuuid)
    rdb.hset('uuid2input', xuuid, xinput.encode('utf8'))
    rdb.hset('uuid2username', xuuid, xusername.encode('utf8'))

    # 等着daemon处理

    # 轮询hash以拿回结果
    while True:
        xoutput = rdb.hget('uuid2output', xuuid)
        if xoutput is None:
            time.sleep(0.001)  # 重要
            continue
        xoutput = xoutput.decode('utf8')
        print('output:', xoutput)
        break


    # 返回输出
    res_json = dict()
    res_json['input'] = xinput
    res_json['output'] = xoutput

    # 清理
    rdb.hdel('uuid2input', xuuid)
    rdb.hdel('uuid2output', xuuid)

    return res_json


if '__main__' == __name__:
    # 启动方式1： 启动命令
    # flask run --host=0.0.0.0 --port=7777

    # 启动方式2： 在这里启动
    # https://www.cnblogs.com/chaojiyingxiong/p/14988069.html
    app.run('0.0.0.0', 7777)
