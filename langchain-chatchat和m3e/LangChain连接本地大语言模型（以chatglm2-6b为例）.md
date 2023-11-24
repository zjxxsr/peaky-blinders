### LangChain连接本地大语言模型（以chatglm2-6b为例）

##### 参考：[LangChain大模型应用落地实践（二）：使用LLMs模块接入自定义大模型，以ChatGLM为例_手把手教你学AI的博客-CSDN博客](https://blog.csdn.net/zhaomengsen/article/details/130585397?ops_request_misc=&request_id=&biz_id=102&utm_term=langchain如何连接本地大模型&utm_medium=distribute.pc_search_result.none-task-blog-2~all~sobaiduweb~default-1-130585397.142^v93^chatsearchT3_2&spm=1018.2226.3001.4187)

#### 一、部署本地模型chatglm2-6b

##### 1.直接从huggingface模型仓库拉取模型文件

```
git clone https://huggingface.co/THUDM/chatglm-6b
```

##### 2.**模型本地调用**

```
import os

from transformers import AutoTokenizer, AutoModel

tokenizer = AutoTokenizer.from_pretrained("THUDM/chatglm-6b", trust_remote_code=True)
model = AutoModel.from_pretrained("THUDM/chatglm-6b", trust_remote_code=True).half().cuda()
model = model.eval()
human_input = "你好"
response, history = model.chat(tokenizer, human_input, history=[])

print(f"Human: {human_input}")
print(f"AI: {response}")
```

#### 二、封装api服务（基于Flask）

模型服务代码如下

```
import os
import json
from flask import Flask
from flask import request 
from transformers import AutoTokenizer, AutoModel


tokenizer = AutoTokenizer.from_pretrained("THUDM/chatglm-6b", trust_remote_code=True)
model = AutoModel.from_pretrained("THUDM/chatglm-6b", trust_remote_code=True).half().cuda()
model.eval()

app = Flask(__name__)

@app.route("/chat", methods=["POST"])
def chat():
    """chat
    """
    data_seq = request.get_data()
    data_dict = json.loads(data_seq)
    human_input = data_dict["human_input"]

    response, _ = model.chat(tokenizer, human_input, history=[])
     
    result_dict = {
        "response": response
    }
    result_seq = json.dumps(result_dict, ensure_ascii=False)
    return result_seq

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8595, debug=False)
```

三、ssh隧道

[AutoDL帮助文档](https://www.autodl.com/docs/ssh_proxy/)

#### 四、使用LangChain调用ChatGLM2-6b



```
import time
import logging
import requests
from typing import Optional, List, Dict, Mapping, Any
 
import langchain
from langchain.llms.base import LLM
from langchain.cache import InMemoryCache
 
logging.basicConfig(level=logging.INFO)
# 启动llm的缓存
langchain.llm_cache = InMemoryCache()
 
class ChatGLM(LLM):
    
    # 模型服务url
    url = "http://127.0.0.1:8595/chat"
 
    @property
    def _llm_type(self) -> str:
        return "chatglm"
 
    def _construct_query(self, prompt: str) -> Dict:
        """构造请求体
        """
        query = {
            "human_input": prompt
        }
        return query
 
    @classmethod
    def _post(cls, url: str,
        query: Dict) -> Any:
        """POST请求
        """
        _headers = {"Content_Type": "application/json"}
        with requests.session() as sess:
            resp = sess.post(url, 
                json=query, 
                headers=_headers, 
                timeout=60)
        return resp
 
    
    def _call(self, prompt: str, 
        stop: Optional[List[str]] = None) -> str:
        """_call
        """
        # construct query
        query = self._construct_query(prompt=prompt)
 
        # post
        resp = self._post(url=self.url,
            query=query)
        
        if resp.status_code == 200:
            resp_json = resp.json()
            predictions = resp_json["response"]
            return predictions
        else:
            return "请求模型" 
    
    @property
    def _identifying_params(self) -> Mapping[str, Any]:
        """Get the identifying parameters.
        """
        _param_dict = {
            "url": self.url
        }
        return _param_dict
 
if __name__ == "__main__":
    llm = ChatGLM()
    while True:
        human_input = input("Human: ")
 
        begin_time = time.time() * 1000
        # 请求模型
        response = llm(human_input, stop=["you"])
        end_time = time.time() * 1000
        used_time = round(end_time - begin_time, 3)
        logging.info(f"chatGLM process time: {used_time}ms")
 
        print(f"ChatGLM: {response}")
```



