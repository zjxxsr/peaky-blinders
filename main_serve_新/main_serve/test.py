import requests

# 定义请求url和传入的data
url = "http://127.0.0.1:5000/v1/main_serve/"
# data = {"uid":"1888254", "text": "肚子痛"}
# data = {"uid":"1888254", "text": "最近我有点不舒服"}
data = {"uid":"1888254", "text": "鼻出血"}

# 向服务发送post请求
res = requests.post(url, data=data)
# 打印返回的结果
print(res.text)

print('-------------------------------------------------')
data1 = {"uid":"1888254", "text": "我今天有点感冒"}

# 向服务发送post请求
res = requests.post(url, data=data1)
# 打印返回的结果
print(res.text)
print('-------------------------------------------------')
data2 = {"uid":"1888254", "text": "小明今天大小便失禁"}

# 向服务发送post请求
res = requests.post(url, data=data2)
# 打印返回的结果
print(res.text)