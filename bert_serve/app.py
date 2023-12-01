from fastapi import FastAPI
app = FastAPI()
import uvicorn
import torch
# 导入中文预训练模型编码函数
from bert_chinese_encode import get_bert_encode
# 导入微调网络
from finetuning_net import Net

# 导入训练好的模型
MODEL_PATH = r"D:\生涯项目文件\NLP53.0\ai13bj\doctor_online\bert_serve\model\BERT_net.pth"
# 定义实例化模型参数
embedding_size = 768
char_size = 20
dropout = 0.2

# 初始化网络
net = Net(embedding_size=embedding_size, char_size=char_size, dropout=dropout)

# 加载模型参数
net.load_state_dict(torch.load(MODEL_PATH))

# 使用评估模式
net.eval()

# 定义接口，这里是通过网络请求到这里的，不是函数调用
@app.post('/v1/recognition/')
def recognition(text1,text2):



    print("recognition:", text1, text2)
    # #对文本进行编码
    # text1= "人生该如何起头"
    # text2= "改变要如何起手"
    inputs = get_bert_encode(text1, text2, mark=102, max_len=10)

    # 把编码输入到模型
    outputs = net(inputs)

    # 获得预测结果
    _, predicted = torch.max(outputs, 1)
    print(predicted)
    print(predicted.shape)
    # 返回结果
    return str(predicted.item())

if __name__ == '__main__':
    print("主题模型开启")
    uvicorn.run(app,host='127.0.0.1', port=5001)

    # 测试模型
    # # 导入训练好的模型
    # MODEL_PATH = "./model/BERT_net.pth"
    # # 定义实例化模型参数
    # embedding_size = 768
    # char_size = 20
    # dropout = 0.2
    #
    # # 初始化网络
    # net = Net(embedding_size=embedding_size, char_size=char_size, dropout=dropout)
    #
    # # 加载模型参数
    # net.load_state_dict(torch.load(MODEL_PATH))
    #
    # # 使用评估模式
    # net.eval()
    # text1= "人生该如何起头"
    # text2= "改变要如何起手"
    # inputs = recognition(text1, text2)
    # print(inputs)
    #
    # # 把编码输入到模型
    # outputs = net(inputs)
    # _, predicted = torch.max(outputs, 1)
    # print(str(predicted.item()))














