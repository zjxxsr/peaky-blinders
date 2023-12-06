from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
import uvicorn
from util import md5, uuid
import redis
import time
import asyncio

app = FastAPI()
rdb = redis.Redis('127.0.0.1', 6379, 0)
PWD = 'my_password_001'


@app.post("/api", response_class=JSONResponse)
async def do_infer(request: Request):
    req_json = await request.json()  # 请求json

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
            await asyncio.sleep(0.001)  # 重要
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

    # https://stackoverflow.com/questions/71794990/fast-api-how-to-return-a-str-as-json
    return JSONResponse(content=res_json)


if '__main__' == __name__:
    # https://stackoverflow.com/questions/63177681/is-there-a-difference-between-running-fastapi-from-uvicorn-command-in-dockerfile
    uvicorn.run('app:app', host='0.0.0.0', port=7777)
