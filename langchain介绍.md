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



# 