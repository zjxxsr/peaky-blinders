import requests
import json
from util import md5

PWD = 'my_password_001'


def text_gen(xinput, xusername=''):
    xjson = dict()
    xjson['input'] = xinput
    xjson['check'] = md5(xinput + PWD)

    res = requests.post('http://127.0.0.1:7777/api', json=xjson)
    xjson = json.loads(res.text)
    xouput = xjson['output']
    return xouput


if '__main__' == __name__:
    x = '您好，请问今天天气如何？'
    r = text_gen(x)
    print(x, '->', r)

    x = '请问顺义八维怎么走？'
    r = text_gen(x)
    print(x, '->', r)
    