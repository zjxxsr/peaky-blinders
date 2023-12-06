import requests
import json


def text_gen(xinput, xusername=''):
    xjson = dict()
    xjson['input'] = xinput

    res = requests.post('http://127.0.0.1:7777/api', json=xjson)
    xjson = json.loads(res.text)
    xouput = xjson['output']
    return xouput


if '__main__' == __name__:
    r = text_gen('您好，请问今天天气如何？')
    print(r)
    r = text_gen('您好，请问顺义八维怎么走？')
    print(r)
    