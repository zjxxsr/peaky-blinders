from elasticsearch import Elasticsearch
es = Elasticsearch(timeout=30)


import json
import os

input_path_review = r'D:\生涯项目文件\NLP53.0\ai13bj\doctor_offline\structured\reviewed'
csv_list = os.listdir(input_path_review)

# 创建索引
result = es.indices.create(index='doctor', ignore=400)

# # 创建数据
# for csv in csv_list:
#     with open(os.path.join(input_path_review, csv), 'r', encoding='utf-8') as fr:
#         all = fr.readlines()
#         for i in all:
#             i = i.replace('\n', '')
#             if len(i) > 0:
#                 data = {'title': i,
#                         }
#
#
#
#                 # 创建ES
#                 es.index(index='doctor', doc_type='symptom', body=data)


# # ES检索工具检索
# result1 = es.search(index='doctor', doc_type='symptom')
# print(result1)


# # ES检索工具检索带条件

def es_search_symptom(text):
    dsl = {
        'query': {
            'match': {
                # 'title': f"cosineSimilarity(params.query_vector, {text}) + 1.0"
                'title': text
            }
        }
    }
    # es = Elasticsearch()
    result2 = es.search(index='doctor', doc_type='symptom', body=dsl)

    max_score = result2['hits']['max_score']
    end_str=[]
    for i in result2['hits']['hits']:
        end_str = i['_source']['title']

        break
    return max_score, end_str

# res = es_search_symptom('今天头很痛')
# print('-------------------------')
# print(res)
#
# end_result=json.dumps(es_search_symptom('我有点头痛'), indent=2, ensure_ascii=False)
# print(end_result)
# ----------------------------------------------------------------------
# # 最大得分
# max_score = es_search_symptom('我有点头痛')['hits']['max_score']
# print(max_score)
# for i in es_search_symptom('我有点头痛')['hits']['hits']:
#     print(i['_source']['title'])
#     break
#
# print([i for i in es_search_symptom('我有点头痛')['hits']['hits']] )
# -------------------------------------------------------------------------------
#
# print('--------------')
# print(es_search_symptom('我有点头痛'))
#
#
# print(es_search_symptom('我有点头痛')['total'])
# 删除索引
#
# result = es.indices.delete(index='doctor', ignore=[400, 404])
# print(result)
