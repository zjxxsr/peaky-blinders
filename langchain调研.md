# langchain调研

### 什么是langchain

LangChain是一个强大的框架，旨在帮助开发人员使用语言模型构建端到端的应用程序。它提供了一系列工具、组件和接口，可简化创建由大型语言模型 (LLM) 和聊天模型提供支持的应用程序的过程。LangChain 可以轻松管理与语言模型的交互，将多个组件链接在一起，并集成额外的资源，例如 API 和数据库。
官方文档：https://python.langchain.com/en/latest/
中文文档：https://www.langchain.com.cn/

### 如何使用langchain

要使用 LangChain，开发人员首先要导入必要的组件和工具，例如 LLMs, chat models, agents, chains, 内存功能。这些组件组合起来创建一个可以理解、处理和响应用户输入的应用程序。

LangChain 为特定用例提供了多种组件，例如个人助理、文档问答、聊天机器人、查询表格数据、与 API 交互、提取、评估和汇总。


### langchain的模型

LangChain model 是一种抽象，表示框架中使用的不同类型的模型。LangChain 中的模型主要分为三类：
1.LLM（大型语言模型）：这些模型将文本字符串作为输入并返回文本字符串作为输出。它们是许多语言模型应用程序的支柱。
2.聊天模型( Chat Model)：聊天模型由语言模型支持，但具有更结构化的 API。他们将聊天消息列表作为输入并返回聊天消息。这使得管理对话历史记录和维护上下文变得容易。
3.文本嵌入模型(Text Embedding Models)：这些模型将文本作为输入并返回表示文本嵌入的浮点列表。这些嵌入可用于文档检索、聚类和相似性比较等任务。

### langchain的主要概念（重点）

●**组件和链**:在LangChain中,组件是模块化的构建块，可以组合起来创建强大的应用程序。链是一系列组合在一起以完成特定任务的组件。

●**提示模板和值:**提示模板负责创建提示值，这是最终传递给语言模型的内容。提示模板可以将用户输入和其他动态信息转换为适合语言模型的格式。

●**示例选择器**:当你想要在提示中动态包含示例时，示例选择器很有用。他们接受用户输入并返回-个示例列表以在提示中使用。

●**输出解析器**:输出解析器负责将语言模型响应构建为更有用的格式。这使得在你的应用程序中处理输出数据变得更加容易。

● **索引和检索器**:索引是一种组织文档的方式，使语言模型更容易与它们交互。检索器是用于获取相关文档并将它们与语言模型组合的接口.

●**聊天消息历史记录**: LangChain主要通过聊天界面与语言模型进行交互。ChatMessageHistory类负责记住所有以前的聊天交互数据，然后可以将这些交互数据传递回模型，这有助于维护上下文并提高模型对对话的理解。

●**代理和工具包**:代理是在LangChain中推动决策制定的实体。他们可以访问一套工具，并可以根据用户输入决定调用哪个工具。工具包是一组工具，当它们一起使用时，可以完成特定的任务。

### 大语言模型的限制

**大型语言模型，如GPT-4, 尽管已经非常强大，但是仍然存在一些限制。以下是几个主要的限制:**

●**知识更新**:大型语言模型的知识是基于其训练数据的。这意味着，-旦训练完毕，模型的知识就固定下来了，不能再进行更新。例如，GPT-4的知识截至日期是2021年，关于之后的事件或者发展它是无法知道的,

●**理解深度**:虽然这类模型可以生成准确的、上下文相关的文本，但它们并不能理解这些文本的深层含义,只是基于它们在大量文本数据,上的训练来模仿人类的问题。

● **事实准确性**:大型语言模型可能会生成一些事实上不准确的信息。因为它们的目标是预测下一一个词是什么，而不是确保生成的所有信息都是准确的。

●**偏见和公平性问题**:大型语言模型可能会反映出其训练数据中的偏见。例如，如果训练数据中存在性别、种族或宗教的偏见，模型可能也会展现出这种偏见。

●**难以解释**:大型语言模型的工作原理非常复杂，这使得它们的预测结果往往难以解释。

●**数据隐私问题**:虽然大型语言模型是在公共数据集上进行训练的，但是由于这些数据集可能含有用户的个人信息，所以在使用这类模型时需要考虑数据隐私的问题。

●**生成恶意内容的风险**:这些模型可以被用来生成深度伪造内容或者恶意信息，从而被用于网络攻击、欺诈或者误导信息的传播。

比如知识不更新，langchain就帮我们接入搜索引擎或者新闻站点

比如理解的深度不够，那我们就编写思维链，一步步引导它完成整个思维过程的推导

比如准确性不够，那我们就接入知识图谱，知识百科，以及专业的知识库

LangChain提供了多种模型,包括大型语言模型、聊天模型和文本嵌入模型。这些模型可以根据应用程序的需求进行选择和使用，总的来说，LangChain是一个强大的框架，可以帮助开发者更轻松地使用大型语言模型来构建应用程序。通过理解和利用上述的核心概念,开发者可以使用LangChain来构建高度适应性、高效且能够处理复杂用例的应用程序。

### 使用示例

#### 直接调用chatAPI:OpenAI

```
#直接调用chatAPI:OpenAI
import openai   #如果没有这个库，需要先安装这个库： pip install openai
openai_api_key = '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'

openai.api_key = openai_api_key
def get_completion(prompt,model = 'gpt-3.5-turbo'):
    messages = [{'role':'user','content':prompt}]
    response = openai.ChatCompletion.create(model = model,
                                            messages = messages,
                                            temperature = 0)
    return response.choices[0].message['content']

if __name__ == '__main__':
    print(get_completion('1+1是什么？'))
```

#### langchain调用openAI

```
#首先，安装LangChain。只需要运行以下命令： pip install langchain


from langchain.chat_models import ChatOpenAI
from  langchain.schema import HumanMessage,SystemMessage,AIMessage

openai_api_key = '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'
chat = ChatOpenAI(temperature=0.7,openai_api_key = openai_api_key)
\#单轮对话示例
answer = chat([
    SystemMessage(content='你是一个很棒的粤菜点餐的人工智能机器人，可以帮助用户在一个简短的句子中弄起给出吃什么！'),
    HumanMessage(content= '我喜欢西红柿我应该吃什么？')
])
print(answer)

\#多轮对话示例
answer1 = chat([
    SystemMessage(content = '你是一个很好的AI机器人，可以帮助用户在一个简短的句子中找出去哪里旅行'),
    HumanMessage(content = '我喜欢海滩，我因该去哪里？'),
    AIMessage(content = '你应该去广东深圳'),
    HumanMessage(content = '当我在那里时我还因该做什么？')
])
print(answer1)
```



#### 构建语言模型应用程序：LLM

    # 导入LLM包装器。
    from langchain.llms import OpenAI
    # 初始化包装器，temperature越高结果越随机
    llm = OpenAI(temperature=0.9)
    # 进行调用
    text = "What would be a good company name for a company that makes colorful socks?"
    print(llm(text))
    #生成结果，结果是随机的 例如： Glee Socks. Rainbow Cozy SocksKaleidoscope Socks.

#### Prompt Templates: 管理LLMs的Prompts

一般来说我们不会直接把输入给模型，而是将输入和一些别的句子连在一起，形成prompts之后给模型。
例如之前根据产品取名的用例，在实际服务中我们可能只想输入"socks"，那么"What would be a good company name for a company that makes"就是我们的template。

    from langchain.llms import OpenAI
    
    openai_api_key = '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'
    llm = OpenAI(model_name='gpt-3.5-turbo-0613',openai_api_key = openai_api_key)
    prompt = '今天是星期一，明天是星期三。这说法有什么问题吗？'
    print(llm(prompt))


​    
​    from langchain import PromptTemplate
​    
    template = '我真的很想去{location}旅行。我应该在那里做什么？'
    prompt = PromptTemplate(input_variables = ['location'],template = template)
    final_prompt = prompt.format(location = '广东广州')
    print(llm(final_prompt))



对于聊天模型，您还可以通过使用 MessagePromptTemplate 来使用模板。您可以从一个或多个 MessagePromptTemplates 创建 ChatPromptTemplate。ChatPromptTemplate 的方法format_prompt返回一个 PromptValue，您可以将其转换为字符串或 Message 对象，具体取决于您是否要使用格式化值作为 LLM 或聊天模型的输入。

```
from langchain.chat_models import ChatOpenAI
from langchain.prompts.chat import (
    ChatPromptTemplate,
    SystemMessagePromptTemplate,
    HumanMessagePromptTemplate,
)
chat = ChatOpenAI(temperature=0)
template="You are a helpful assistant that translates {input_language} to {output_language}."
system_message_prompt = SystemMessagePromptTemplate.from_template(template)
human_template="{text}"
human_message_prompt = HumanMessagePromptTemplate.from_template(human_template)
chat_prompt = ChatPromptTemplate.from_messages([system_message_prompt, human_message_prompt])

# get a chat completion from the formatted messages

chat(chat_prompt.format_prompt(input_language="English", output_language="Chinese", text="I love programming.").to_messages())

# -> AIMessage(content="我喜欢编程。(Wǒ xǐhuān biānchéng.)", additional_kwargs={})
```



探索将内存与使用聊天模型初始化的链和代理一起使用。这与 Memory for LLMs 的主要区别在于我们可以将以前的消息保留为它们自己唯一的内存对象，而不是将它们压缩成一个字符串。

```
from langchain.prompts import (
    ChatPromptTemplate, 
    MessagesPlaceholder, 
    SystemMessagePromptTemplate, 
    HumanMessagePromptTemplate
)
from langchain.chains import ConversationChain
from langchain.chat_models import ChatOpenAI
from langchain.memory import ConversationBufferMemory

prompt = ChatPromptTemplate.from_messages([
    SystemMessagePromptTemplate.from_template("下面是一段人类和人工智能之间的友好对话。人工智能滔滔不绝，并根据上下文提供了许多具体细节。如果人工智能不知道问题的答案，它就会如实说不知道。"),
    MessagesPlaceholder(variable_name="history"),
    HumanMessagePromptTemplate.from_template("{input}")
])


openai_api_key = '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'
llm = ChatOpenAI(temperature=0,openai_api_key=openai_api_key)
memory = ConversationBufferMemory(return_messages=True)
conversation = ConversationChain(memory=memory, prompt=prompt, llm=llm)
result1 = conversation.predict(input="你好！")
print(result1)

result2 = conversation.predict(input="我做得很好！只是在和人工智能对话")
print(result2)

result3 = conversation.predict(input="河南在哪里")
print(result3)
   
```



#### 顺序链

```
from langchain.llms import OpenAI
from langchain.chains import LLMChain
from langchain.prompts import PromptTemplate
from langchain.chains import SimpleSequentialChain

openai_api_key = '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'
llm = OpenAI(temperature = 1,openai_api_key = openai_api_key)

template_location = '''您的工作是根据用户建议的区域制作一道经典菜肴。
%用户位置
{user_location}
AI回答：
'''
prompt_template = PromptTemplate(input_variables=['user_location'],template=template_location)
location_chain = LLMChain(llm=llm,prompt=prompt_template)


template_meal = '''给出一个简短的食谱，说明如何在家做这道菜
%菜谱
{user_meal}
AI回答：
'''
prompt_template = PromptTemplate(input_variables=['user_meal'],template=template_meal)
meal_chain = LLMChain(llm=llm,prompt = prompt_template)

overall_chain = SimpleSequentialChain(chains = [location_chain,meal_chain],verbose=True)

review = overall_chain.run('广东广州')

print(review)


```



[LangChain入门指南_故里_的博客-CSDN博客](https://blog.csdn.net/lht0909/article/details/130412875?ops_request_misc=%7B%22request%5Fid%22%3A%22169140245816800188585374%22%2C%22scm%22%3A%2220140713.130102334..%22%7D&request_id=169140245816800188585374&biz_id=0&utm_medium=distribute.pc_search_result.none-task-blog-2~all~top_positive~default-3-130412875-null-null.142^v92^controlT0_2&utm_term=langchain&spm=1018.2226.3001.4187)

【【开发必看】AI应用开发LangChain系列课程】https://www.bilibili.com/video/BV1Uh4y1X76G?p=6&vd_source=889b96aa4eb69fbbb0f6b0354dd49949

