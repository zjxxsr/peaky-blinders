import requests

url = "http://127.0.0.1:5001/v1/recognition/"
data = {"text1":"你好小仇", "text2": "你好先生"}
res = requests.post(url, data=data)

print("预测样本:", data["text1"], "|", data["text2"])
print("预测结果:", res.text)
