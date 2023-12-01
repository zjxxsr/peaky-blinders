REDIS_CONFIG = {
     "host": "127.0.0.1", # 修改
     "port": 6379
}


NEO4J_CONFIG = {
    "uri": "bolt://127.0.0.1:7687",
    "auth": ("neo4j", '12345678'),
    "encrypted": False
}

model_serve_url = "http://127.0.0.1:5001/v1/recognition/"

TIMEOUT = 100

reply_path = "./reply.json"

ex_time = 36000    #秒

bert_model = r"D:\生涯项目文件\NLP53.0\ai13bj\doctor_offline\bert-base-chinese"