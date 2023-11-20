import requests
import json
url="http://127.0.0.1:8000/zjx"

input_key=input("请输入一个key:")
input_values=input("请输入一个values:")
data_dict=dict()

data_dict[input_key]=input_values
with open("flask_json.json","w",encoding="utf8") as f:
    json.dump(data_dict,f,ensure_ascii=False)

file=open("flask_json.json","r",encoding="utf8")
print("file:",file)
print(type(file))
result=json.load(file)
print("result:",result)
print(type(result))

res=requests.post(url,json=result)
print("res.text type:",type(res.text))
xres=json.loads(res.text)
print(xres)
print(type(xres))




