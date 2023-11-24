# langchain介绍

### 什么是LangChain

LangChain是一个强大的框架，旨在帮助开发人员使用语言模型构建端到端的应用程序。它提供了一套工具、组件和接口，可简化创建由大型语言模型 (LLM) 和聊天模型提供支持的应用程序的过程。LangChain 可以轻松管理与语言模型的交互，将多个组件链接在一起，并集成额外的资源，例如 API 和数据库。

![9341203639d24acd8d8dcc9caf098451.png](https://img-blog.csdnimg.cn/9341203639d24acd8d8dcc9caf098451.png)

```
Model： 借助 LangChain，与大语言模型的交互变得更加便捷，LangChain 还提供了异步支持 
Prompt： 包括提示管理、提示优化和提示序列化 
Memory： LangChain 提供了辅助工具，用于管理和操作先前的聊天消息，这些工具设计成模块化的，无论用例如何，都能很好地使用。
Chain： 链式（Chain）提供了将各种组件合并成一个统一应用程序的方式。
Agent： 代理可以访问多种工具。根据用户的输入，代理可能决定是否调用这些工具，并确定调用时的输入。
index： 语言模型在与自己的文本数据结合时往往更强大

```

![065897a7bf4088ba2a036ff02780910a.jpeg](https://img-blog.csdnimg.cn/img_convert/065897a7bf4088ba2a036ff02780910a.jpeg)

agent运行流程图

![img](https://img-blog.csdnimg.cn/a7be51e9a2174fdd97a1cfc6c7a3ea3a.png)

langchain原理图示：

![image-20230819101843782](C:\Users\白旭瑜\AppData\Roaming\Typora\typora-user-images\image-20230819101843782.png)

### 如何使用 LangChain？

要使用 LangChain，开发人员首先要导入必要的组件和工具，例如 LLMs, chat models, agents, chains, 内存功能。这些组件组合起来创建一个可以理解、处理和响应用户输入的应用程序。

LangChain 为特定用例提供了多种组件，例如个人助理、文档问答、聊天机器人、查询表格数据、与 API 交互、提取、评估和汇总。

### LangChain 中的模型主要分为三类：

1.LLM（大型语言模型），这些模型将文本字符串作为输入并返回文本字符串作为输出。它们是许多语言模型应用程序的支柱。

2.聊天模型( Chat Model)，聊天模型由语言模型支持，但具有更结构化的 API。他们将聊天消息列表作为输入并返回聊天消息。这使得管理对话历史记录和维护上下文变得容易。

3.文本嵌入模型(Text Embedding Models)，这些模型将文本作为输入并返回表示文本嵌入的浮点列表。这些嵌入可用于文档检索、聚类和相似性比较等任务。

![img](https://img-blog.csdnimg.cn/9c2e9d96d85e4214aff7006b395a3408.png)

### 功能简介

#### Prompts 提示管理

```
PromptTemplate` 可以生成文本模版，通过变量参数的形式拼接成完整的语句。

FewShotPromptTemplate 选择器示例，将提示的示例内容同样拼接到语句中，让模型去理解语义含义进而给出结果

ChatPromptTemplate 聊天提示模版，以聊天消息作为输入生成完整提示模版。

StructuredOutputParser 输出解析器，要使 `LLM` 模型返回我们需要的格式，可以直接告诉 `LLM` 你想要的结果格式，也可以通过 解析器来制定：
PromptTemplate + StructuredOutputParser
PromptTemplate + ChatPromptTemplate
```

#### 文件载入 和 Embeddings 文本向量化

```
文件加载与分割：自己进行文件的加载，然后对字符串进行分割
Embeddings 文本向量化：可以计算出文本的相似性
```

#### memory 多轮对话

```
对于聊天应用中，记录聊天的记录给到模型可以回答出更加准确的回答，还可以基于 Memory 组件中的 ChatMessageHistory 
```

### chain 顺序链

```
1.简单顺序链  可以使用 LLM 的输出作为另一个 LLM 的输入。有利于任务的分解：
2.总结链  有时候对于大量的文本内容进行摘要总结，可能无法一次性加载进来，此时可借助总结链进行总结：
```

### 问答

```
通过本地知识库微调模型，回答出更加准确的信息。
```



# LangChain-ChatGLM

https://mp.weixin.qq.com/s/FqehXo3u5zdhiAWVa-31lw

https://github.com/chatchat-space/Langchain-Chatchat/tree/master

本项目已在 Python 3.8.1 - 3.10，CUDA 11.7 环境下完成测试。已在 Windows、ARM 架构的 macOS、Linux 系统中完成测试。



## 项目介绍

一种利用 [langchain](https://github.com/hwchase17/langchain) 思想实现的基于本地知识库的问答应用，目标期望建立一套对中文场景与开源模型支持友好、可离线运行的知识库问答解决方案。

本项目实现原理如下图所示，过程包括加载文件 -> 读取文本 -> 文本分割 -> 文本向量化 -> 问句向量化 -> 在文本向量中匹配出与问句向量最相似的 `top k`个 -> 匹配出的文本作为上下文和问题一起添加到 `prompt`中 -> 提交给 `LLM`生成回答。

![langchain+chatglm.png](https://github.com/chatchat-space/Langchain-Chatchat/blob/master/img/langchain+chatglm.png?raw=true)

从文档处理角度来看，实现流程如下：

![langchain+chatglm2.png](https://github.com/chatchat-space/Langchain-Chatchat/blob/master/img/langchain+chatglm2.png?raw=true)



## 云服务器部署注意事项：

[AutoDL 镜像](https://www.codewithgpu.com/i/imClumsyPanda/langchain-ChatGLM/Langchain-Chatchat) 中 `v5` 版本所使用代码已更新至本项目 `0.2.0` 版本。

```
https://www.codewithgpu.com/i/imClumsyPanda/langchain-ChatGLM/Langchain-Chatchat
```

[Docker 镜像](https://github.com/chatchat-space/Langchain-Chatchat/blob/master/registry.cn-beijing.aliyuncs.com/chatchat/chatchat:0.2.0)

💻 一行命令运行 Docker：

```
docker run -d --gpus all -p 80:8501 registry.cn-beijing.aliyuncs.com/chatchat/chatchat:0.2.0
```



## 变更日志

### `0.2.0` 版本与 `0.1.x` 版本区别

1. 使用 [FastChat](https://github.com/lm-sys/FastChat) 提供开源 LLM 模型的 API，以 OpenAI API 接口形式接入，提升 LLM 模型加载效果；
2. 使用 [langchain](https://github.com/langchain-ai/langchain) 中已有 Chain 的实现，便于后续接入不同类型 Chain，并将对 Agent 接入开展测试；
3. 使用 [FastAPI](https://github.com/tiangolo/fastapi) 提供 API 服务，全部接口可在 FastAPI 自动生成的 docs 中开展测试，且所有对话接口支持通过参数设置流式或非流式输出；
4. 使用 [Streamlit](https://github.com/streamlit/streamlit) 提供 WebUI 服务，可选是否基于 API 服务启动 WebUI，增加会话管理，可以自定义会话主题并切换，且后续可支持不同形式输出内容的显示；
5. 项目中默认 LLM 模型改为 [THUDM/chatglm2-6b](https://huggingface.co/THUDM/chatglm2-6b)，默认 Embedding 模型改为 [moka-ai/m3e-base](https://huggingface.co/moka-ai/m3e-base)，文件加载方式与文段划分方式也有调整，后续将重新实现上下文扩充，并增加可选设置；
6. 项目中扩充了对不同类型向量库的支持，除支持 [FAISS](https://github.com/facebookresearch/faiss) 向量库外，还提供 [Milvus](https://github.com/milvus-io/milvus), [PGVector](https://github.com/pgvector/pgvector) 向量库的接入；
7. 项目中搜索引擎对话，除 Bing 搜索外，增加 DuckDuckGo 搜索选项，DuckDuckGo 搜索无需配置 API Key，在可访问国外服务环境下可直接使用。

## 模型支持

本项目中默认使用的 LLM 模型为 [THUDM/chatglm2-6b](https://huggingface.co/THUDM/chatglm2-6b)，默认使用的 Embedding 模型为 [moka-ai/m3e-base](https://huggingface.co/moka-ai/m3e-base) 为例。

### LLM 模型支持

本项目最新版本中基于 [FastChat](https://github.com/lm-sys/FastChat) 进行本地 LLM 模型接入，支持模型如下：

- [meta-llama/Llama-2-7b-chat-hf](https://huggingface.co/meta-llama/Llama-2-7b-chat-hf)
- Vicuna, Alpaca, LLaMA, Koala
- [BlinkDL/RWKV-4-Raven](https://huggingface.co/BlinkDL/rwkv-4-raven)
- [camel-ai/CAMEL-13B-Combined-Data](https://huggingface.co/camel-ai/CAMEL-13B-Combined-Data)
- [databricks/dolly-v2-12b](https://huggingface.co/databricks/dolly-v2-12b)
- [FreedomIntelligence/phoenix-inst-chat-7b](https://huggingface.co/FreedomIntelligence/phoenix-inst-chat-7b)
- [h2oai/h2ogpt-gm-oasst1-en-2048-open-llama-7b](https://huggingface.co/h2oai/h2ogpt-gm-oasst1-en-2048-open-llama-7b)
- [lcw99/polyglot-ko-12.8b-chang-instruct-chat](https://huggingface.co/lcw99/polyglot-ko-12.8b-chang-instruct-chat)
- [lmsys/fastchat-t5-3b-v1.0](https://huggingface.co/lmsys/fastchat-t5)
- [mosaicml/mpt-7b-chat](https://huggingface.co/mosaicml/mpt-7b-chat)
- [Neutralzz/BiLLa-7B-SFT](https://huggingface.co/Neutralzz/BiLLa-7B-SFT)
- [nomic-ai/gpt4all-13b-snoozy](https://huggingface.co/nomic-ai/gpt4all-13b-snoozy)
- [NousResearch/Nous-Hermes-13b](https://huggingface.co/NousResearch/Nous-Hermes-13b)
- [openaccess-ai-collective/manticore-13b-chat-pyg](https://huggingface.co/openaccess-ai-collective/manticore-13b-chat-pyg)
- [OpenAssistant/oasst-sft-4-pythia-12b-epoch-3.5](https://huggingface.co/OpenAssistant/oasst-sft-4-pythia-12b-epoch-3.5)
- [project-baize/baize-v2-7b](https://huggingface.co/project-baize/baize-v2-7b)
- [Salesforce/codet5p-6b](https://huggingface.co/Salesforce/codet5p-6b)
- [StabilityAI/stablelm-tuned-alpha-7b](https://huggingface.co/stabilityai/stablelm-tuned-alpha-7b)
- [THUDM/chatglm-6b](https://huggingface.co/THUDM/chatglm-6b)
- [THUDM/chatglm2-6b](https://huggingface.co/THUDM/chatglm2-6b)
- [tiiuae/falcon-40b](https://huggingface.co/tiiuae/falcon-40b)
- [timdettmers/guanaco-33b-merged](https://huggingface.co/timdettmers/guanaco-33b-merged)
- [togethercomputer/RedPajama-INCITE-7B-Chat](https://huggingface.co/togethercomputer/RedPajama-INCITE-7B-Chat)
- [WizardLM/WizardLM-13B-V1.0](https://huggingface.co/WizardLM/WizardLM-13B-V1.0)
- [WizardLM/WizardCoder-15B-V1.0](https://huggingface.co/WizardLM/WizardCoder-15B-V1.0)
- [baichuan-inc/baichuan-7B](https://huggingface.co/baichuan-inc/baichuan-7B)
- [internlm/internlm-chat-7b](https://huggingface.co/internlm/internlm-chat-7b)
- [Qwen/Qwen-7B-Chat](https://huggingface.co/Qwen/Qwen-7B-Chat)
- [HuggingFaceH4/starchat-beta](https://huggingface.co/HuggingFaceH4/starchat-beta)
- 任何 [EleutherAI](https://huggingface.co/EleutherAI) 的 pythia 模型，如 [pythia-6.9b](https://huggingface.co/EleutherAI/pythia-6.9b)
- 在以上模型基础上训练的任何 [Peft](https://github.com/huggingface/peft) 适配器。为了激活，模型路径中必须有 `peft` 。注意：如果加载多个peft模型，你可以通过在任何模型工作器中设置环境变量 `PEFT_SHARE_BASE_WEIGHTS=true` 来使它们共享基础模型的权重。

以上模型支持列表可能随 [FastChat](https://github.com/lm-sys/FastChat) 更新而持续更新，可参考 [FastChat 已支持模型列表](https://github.com/lm-sys/FastChat/blob/main/docs/model_support.md)。

除本地模型外，本项目也支持直接接入 OpenAI API，具体设置可参考 `configs/model_configs.py.example` 中的 `llm_model_dict` 的 `openai-chatgpt-3.5` 配置信息。

### Embedding 模型支持

本项目支持调用 [HuggingFace](https://huggingface.co/models?pipeline_tag=sentence-similarity) 中的 Embedding 模型，已支持的 Embedding 模型如下：

- [moka-ai/m3e-small](https://huggingface.co/moka-ai/m3e-small)
- [moka-ai/m3e-base](https://huggingface.co/moka-ai/m3e-base)
- [moka-ai/m3e-large](https://huggingface.co/moka-ai/m3e-large)
- [BAAI/bge-small-zh](https://huggingface.co/BAAI/bge-small-zh)
- [BAAI/bge-base-zh](https://huggingface.co/BAAI/bge-base-zh)
- [BAAI/bge-large-zh](https://huggingface.co/BAAI/bge-large-zh)
- [text2vec-base-chinese-sentence](https://huggingface.co/shibing624/text2vec-base-chinese-sentence)
- [text2vec-base-chinese-paraphrase](https://huggingface.co/shibing624/text2vec-base-chinese-paraphrase)
- [text2vec-base-multilingual](https://huggingface.co/shibing624/text2vec-base-multilingual)
- [shibing624/text2vec-base-chinese](https://huggingface.co/shibing624/text2vec-base-chinese)
- [GanymedeNil/text2vec-large-chinese](https://huggingface.co/GanymedeNil/text2vec-large-chinese)
- [nghuyong/ernie-3.0-nano-zh](https://huggingface.co/nghuyong/ernie-3.0-nano-zh)
- [nghuyong/ernie-3.0-base-zh](https://huggingface.co/nghuyong/ernie-3.0-base-zh)

## Docker 部署

🐳 Docker 镜像地址: `registry.cn-beijing.aliyuncs.com/chatchat/chatchat:0.2.0)`

```
docker run -d --gpus all -p 80:8501 registry.cn-beijing.aliyuncs.com/chatchat/chatchat:0.2.0
```

- 该版本镜像大小 `33.9GB`，使用 `v0.2.0`，以 `nvidia/cuda:12.1.1-cudnn8-devel-ubuntu22.04` 为基础镜像
- 该版本内置一个 `embedding` 模型：`m3e-large`，内置 `chatglm2-6b-32k`
- 该版本目标为方便一键部署使用，请确保您已经在Linux发行版上安装了NVIDIA驱动程序
- 请注意，您不需要在主机系统上安装CUDA工具包，但需要安装 `NVIDIA Driver` 以及 `NVIDIA Container Toolkit`，请参考[安装指南](https://docs.nvidia.com/datacenter/cloud-native/container-toolkit/latest/install-guide.html)
- 首次拉取和启动均需要一定时间，首次启动时请参照下图使用 `docker logs -f <container id>` 查看日志
- 如遇到启动过程卡在 `Waiting..` 步骤，建议使用 `docker exec -it <container id> bash` 进入 `/logs/` 目录查看对应阶段日志



## 开发部署：

### 软件需求

本项目已在 Python 3.8.1 - 3.10，CUDA 11.7 环境下完成测试。已在 Windows、ARM 架构的 macOS、Linux 系统中完成测试。

#### 下载源码：

```
https://github.com/chatchat-space/Langchain-Chatchat/tree/master
```

#### 安装依赖：

```
cd langchain-ChatGLM
pip install -r requirements.txt

需要注意的是tensbord，protobuf，streamlit这三个库之间可能因为版本问题会有冲突，推荐先确定streamlit的版本，再更新protobuf的版本，最后更新tensbord的版本
```

#### 下载模型：

```
# 安装 git lfs
git lfs install

# 下载 LLM 模型
git clone https://huggingface.co/THUDM/chatglm2-6b 

# 下载 Embedding 模型
git clone https://huggingface.co/GanymedeNil/text2vec-large-chinese

git clone https://huggingface.co/moka-ai/m3e-base

# 模型需要更新时，可打开模型所在文件夹后拉取最新模型文件/代码
git pull
```

算力云服务器上没有git-lfs的解决方案：

https://www.jianshu.com/p/493b81544f80

```
如果不装Git LFS，模型文件下载不完整
curl -s https://packagecloud.io/install/repositories/github/git-lfs/script.deb.sh | sudo bash

sudo apt-get install git-lfs

git lfs install
```

#### 参数调整：

复制模型相关参数配置模板文件 [configs/model_config.py.example](https://github.com/chatchat-space/Langchain-Chatchat/blob/master/configs/model_config.py.example) 存储至项目路径下 `./configs` 路径下，并重命名为 `model_config.py`。

复制服务相关参数配置模板文件 [configs/server_config.py.example](https://github.com/chatchat-space/Langchain-Chatchat/blob/master/configs/server_config.py.example) 存储至项目路径下 `./configs` 路径下，并重命名为 `server_config.py`。

在开始执行 Web UI 或命令行交互前，请先检查 `configs/model_config.py` 和 `configs/server_config.py` 中的各项模型参数设计是否符合需求：

- 请确认已下载至本地的 LLM 模型本地存储路径写在 `llm_model_dict` 对应模型的 `local_model_path` 属性中，如:

```
llm_model_dict={
                "chatglm2-6b": {
                        "local_model_path": "/Users/xxx/Downloads/chatglm2-6b",
                        "api_base_url": "http://localhost:8888/v1",  # "name"修改为 FastChat 服务中的"api_base_url"
                        "api_key": "EMPTY"
                    },
                }
```



- 请确认已下载至本地的 Embedding 模型本地存储路径写在 `embedding_model_dict` 对应模型位置，如：

```
embedding_model_dict = {
                        "m3e-base": "/Users/xxx/Downloads/m3e-base",
                       }
```

#### 知识库初始化与迁移

- 如果您是第一次运行本项目，知识库尚未建立，或者配置文件中的知识库类型、嵌入模型发生变化，需要以下命令初始化或重建知识库：

  ```
  $ python init_database.py --recreate-vs
  ```

- 如果您是从 `0.1.x` 版本升级过来的用户，针对已建立的知识库，请确认知识库的向量库类型、Embedding 模型 `configs/model_config.py` 中默认设置一致，如无变化只需以下命令将现有知识库信息添加到数据库即可：

  ```
  $ python init_database.py
  ```



#### 启动API服务或Web UI

1.先启动LLM服务

```
python server/llm_api.py
```

2.启动API服务

```
python server/api.py
启动 API 服务后，可访问 localhost:7861 或 {API 所在服务器 IP}:7861 FastAPI 自动生成的 docs 进行接口查看与测试
```

3.启动 Web UI 服务

```
streamlit run webui.py
```

使用 Langchain-Chatchat 主题色启动 **Web UI** 服务（默认使用端口 `8501`）

```
$ streamlit run webui.py --server.port 6006 --theme.base "light" --theme.primaryColor "#165dff" --theme.secondaryBackgroundColor "#f5f5f5" --theme.textColor "#000000"
```

或使用以下命令指定启动 **Web UI** 服务并指定端口号

```
$ streamlit run webui.py --server.port 6006
```



#### 一键启动

更新一键启动脚本 startup.py,一键启动所有 Fastchat 服务、API 服务、WebUI 服务，示例代码：

```
$ python startup.py --all-webui
```

并可使用 `Ctrl + C` 直接关闭所有运行服务。

可选参数包括 `--all-webui`, `--all-api`, `--llm-api`, `--controller`, `--openai-api`, `--model-worker`, `--api`, `--webui`，其中：

- `--all-webui` 为一键启动 WebUI 所有依赖服务；
- `--all-api` 为一键启动 API 所有依赖服务；
- `--llm-api` 为一键启动 Fastchat 所有依赖的 LLM 服务；
- `--openai-api` 为仅启动 FastChat 的 controller 和 openai-api-server 服务；
- 其他为单独服务启动选项。

若想指定非默认模型，需要用 `--model-name` 选项，示例：

```
$ python startup.py --all-webui --model-name Qwen-7B-Chat
```

**注意：**

**1. startup 脚本用多进程方式启动各模块的服务，可能会导致打印顺序问题，请等待全部服务发起后再调用，并根据默认或指定端口调用服务（默认 LLM API 服务端口：`127.0.0.1:8888`,默认 API 服务端口：`127.0.0.1:7861`,默认 WebUI 服务端口：`本机IP：8501`)**

**2.服务启动时间示设备不同而不同，约 3-10 分钟，如长时间没有启动请前往 `./logs`目录下监控日志，定位问题**