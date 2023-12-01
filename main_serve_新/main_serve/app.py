# 服务框架使用Flask
# 导入必备的工具
# from flask import Flask
# from flask import request
import time
from fastapi import FastAPI
import uvicorn
# app = Flask(__name__)

app=FastAPI()
# 导入发送http请求的requests工具
import requests

# 导入操作redis数据库的工具
import redis

# 导入加载json文件的工具
import json

# 导入已写好的Unit API调用文件
from unit import unit_chat

# 导入操作neo4j数据库的工具
from neo4j import GraphDatabase

# 从配置文件中导入需要的配置
# NEO4J的连接配置
from config import NEO4J_CONFIG
# REDIS的连接配置
from config import REDIS_CONFIG
# 句子相关模型服务的请求地址
from config import model_serve_url
# 句子相关模型服务的超时时间
from config import TIMEOUT
# 规则对话模版的加载路径
from config import reply_path
# 用户对话信息保存的过期时间
from config import ex_time
# 自动机机制
from AC_Robot import test_ahocorasick
# ES检索工具
from ES_jiansuo import es_search_symptom
# 建立REDIS连接池
pool = redis.ConnectionPool(**REDIS_CONFIG)

# 初始化NEO4J驱动对象
_driver = GraphDatabase.driver(**NEO4J_CONFIG)


# 数据库查询函数
def neo4j_amtch(text):
    with _driver.session() as session:
        cypher = "MATCH(a:Symptom) WHERE(%r contains a.name) WITH" \
                 " a MATCH(a)-[r:dis_to_sym]-(b:Disease) RETURN b.name LIMIT 5" % text
        record = session.run(cypher)
        result = list(map(lambda x: x[0], record))

    return result

# 根据用户输入的症状进行疾病名称的查询
def query_neo4j(text1):
    """
    :param text: 症状名称
    :return: 对应的疾病名称
    """
    # 广义前缀树 tries
    # KMP算法，字符串匹配

    # 倒排索引，通过关键词

    # 标识
    # 深度了解
    # 代码融合
    # 语言简练
    print('AC自动机前数据：',text1)
    text = test_ahocorasick(text1)
    print('AC自动机后数据：',text)

    # 判断查询后句子长度是否一致
    if text == text1:
        # 进入ES进行检索，返回最高分数和结果
        result = es_search_symptom(text)
        # 返回分数最高值
        max_score = result[0]
        print('ES最大得分:',max_score)
        # 取出检索后的结果
        text = result[1]
        # 结果进入neo4j进行查询
        result2 = neo4j_amtch(text)
        # 返回查询结果
        return result2

    else:
        # 进入neo4j进行查询
        result2 = neo4j_amtch(text)
        # 返回查询结果
        return result2



# 实现处理不同分支函数
class Handler(object):
    def __init__(self, uid, text, r, reply):  # 类内部的函数，第一个参数是self
        self.uid = uid
        self.r = r
        self.text = text
        self.reply = reply

    def non_first_sentence(self, previous):
        # 处理用户非第一次输入
        try:
            print("准备请求句子相关模型服务!")
            data = {'text1': previous, 'text2': self.text}
            result = requests.post(model_serve_url, data=data, timeout=TIMEOUT)
            print("句子相关模型服务请求成功, 返回结果为:", result.text)
            if not result.text: return unit_chat(self.text)
            print()
            # 也可以，如果前后两句没有相关性，把第二句的text放到neo4j中查询
            # 也可以返回查询的结果
            # print("non_first_sentence, unit_chat")
            # return unit_chat(self.text)
        except Exception as e:
            print("模型异常", e)
            return unit_chat(self.text)

        s = query_neo4j(self.text)
        print(s)
        if not s: return unit_chat(self.text)

        old_disease = self.r.hget(str(self.uid), "previous_d")
        if old_disease:
            if set(old_disease) == set(s):   # 修改了一下
                return list(set(old_disease))
            else:
                new_disease = list(set(s) | set(old_disease))
                res = list(set(s) - set(old_disease))  # 在第一个集合中存在且不在第二个集合中存在的元素
        else:
            res = list(set(s))
            new_disease = res

        self.r.hset(str(self.uid), "previous_d", str(new_disease))
        self.r.expire(str(self.uid), ex_time)

        if not res:
            return self.reply['4']
        else:
            res = '，'.join(res)
            return self.reply['2'] % res

    def first_sentence(self):
        # 处理用户第一次输入
        s = query_neo4j(self.text)

        if not s:
            return unit_chat(self.text)

        self.r.hset(str(self.uid), 'previous_d', str(s))
        self.r.expire(str(self.uid), ex_time)  #

        res = "，".join(s)

        return self.reply['2'] % res


# 实现主要逻辑服务，是通过发送post网络请求
# @app.route("/v1/main_serve/", methods=["POST"])
@app.post("/v1/main_serve/")

def main_serve(uid,text):
    # time1 =time.time()#开始时间
    # 接收werobot发送的请求
    # uid = request.form['uid']
    # text = request.form['text']
    print(text)  # -=----------
    # 从redis中获取一个活跃的连接
    r = redis.StrictRedis(connection_pool=pool)

    # 根据用户的uid获取是否存在上一句话
    previous = r.hget(str(uid), 'previous')
    print("main_serve previous:", previous)

    # 设置当前的输入作为上一句
    r.hset(str(uid), 'previous', text)

    # 获取模板
    reply = json.load(open(reply_path, 'r', encoding='utf-8'))  # --------

    # 构造handler，根据是否是第一次请求实现逻辑
    handler = Handler(uid, text, r, reply)
    print(handler)
    # 根据previous是否存在，判断是否是第一句
    time2 = time.time()
    # time_interval = time2 - time1  # 耗时间隔
    # print("耗时:", time_interval)
    if previous:
        return handler.non_first_sentence(previous)
    else:
        return handler.first_sentence()


# # 测试query_neo4j函数
# if __name__ == '__main__':
#     text = "我最近腹痛!"
#     print(query_neo4j(text))

if __name__ == '__main__':
    print('主服务开启')
    # app.run(host='localhost', port=5000)

    uvicorn.run(app,host="127.0.0.1",port=5000)