from transformers import AutoTokenizer,AutoModel

from langchain.document_loaders import UnstructuredFileLoader
from langchain.text_splitter import CharacterTextSplitter
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.vectorstores import FAISS

model_path = r'../模型/langchain-model/chatglm2-6b'
# 启动模型
tokenizer = AutoTokenizer.from_pretrained(model_path,trust_remote_code=True)
model = AutoModel.from_pretrained(model_path,trust_remote_code=True).half().cuda()
chatglm = model.eval()

# 定义文件路径
filepath = "test.txt"

# 加载文件
loader = UnstructuredFileLoader(filepath)
docs = loader.load()

# 文本分割
text_splitter = CharacterTextSplitter(chunk_size=500,chunk_overlap=200)
docs = text_splitter.split_text(docs)

# 构建向量库
embeddings = OpenAIEmbeddings()
vector_store = FAISS.from_documents(docs,embeddings)

# 根据提问匹配上下文
query = "Langchain 能够接入哪些数据类型？"
docs = vector_store.similarity_search(query)
context = [doc.page_content for doc in docs]

# 不知道原本的处理方式，个人理解加的，目的将list转为str
context = ','.join(context)

# 构造 Prompt
prompt = f"已知信息：\n{context}\n根据已知信息回答问题：\n{query}"

# llm 生成回答
chatglm.chat(tokenizer,prompt,history=[])