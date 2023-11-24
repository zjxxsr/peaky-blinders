# M3E调研

M3E，开源中文 Embedding 模型新 SOTA

**M3E Models** ：Moka（北京希瑞亚斯科技）开源的系列**文本嵌入模型**。

M3E Models 是使用千万级 (2200w+) 的中文句对数据集进行训练的 Embedding 模型，在**文本分类和文本检索的任务上都超越了 openai-ada-002 模型（ChatGPT 官方的模型）**。

**项目地址：**

```
m3e-base
https://huggingface.co/moka-ai/m3e-base
m3e-small
https://huggingface.co/moka-ai/m3e-small
```

M3E 是 Moka Massive Mixed Embedding 的缩写

- Moka，此模型由 MokaAI 训练，开源和评测，训练脚本使用 uniem ，评测 BenchMark 使用 MTEB-zh
- Massive，此模型通过**千万级** (2200w+) 的中文句对数据集进行训练
- Mixed，此模型支持中英双语的同质文本相似度计算，异质文本检索等功能，未来还会支持代码检索
- Embedding，此模型是文本嵌入模型，可以将自然语言转换成稠密的向量

## 模型对比

![图片](https://mmbiz.qpic.cn/sz_mmbiz_png/nW2ZPfuYqSLR7icZAIBqJp2IxuGtQU95uI9GUVPFGvmAZ5KGibt3MiaSPa7v8QJe6w96aeRVgUwiaeA4wEiaNZL1adQ/640?wx_fmt=png&wxfrom=5&wx_lazy=1&wx_co=1)

说明：

- s2s, 即 sentence to sentence ，代表了同质文本之间的嵌入能力，适用任务：文本相似度，重复问题检测，文本分类等
- s2p, 即 sentence to passage ，代表了异质文本之间的嵌入能力，适用任务：文本检索，GPT 记忆模块等
- s2c, 即 sentence to code ，代表了自然语言和程序语言之间的嵌入能力，适用任务：代码检索
- 兼容性，代表了模型在开源社区中各种项目被支持的程度，由于 m3e 和 text2vec 都可以直接通过 sentence-transformers 直接使用，所以和 openai 在社区的支持度上相当

Tips:

- 使用场景主要是中文，少量英文的情况，建议使用 m3e 系列的模型
- 多语言使用场景，并且不介意数据隐私的话，我建议使用 openai-ada-002
- 代码检索场景，推荐使用 ada-002

## 使用方式

您需要先安装 sentence-transformers

```
pip install -U sentence-transformers
```

安装完成后，您可以使用以下代码来使用 M3E Models

```
from sentence_transformers import SentenceTransformer

model = SentenceTransformer('moka-ai/m3e-base')

#Our sentences we like to encode
sentences = [
    '* Moka 此文本嵌入模型由 MokaAI 训练并开源，训练脚本使用 uniem',
    '* Massive 此文本嵌入模型通过**千万级**的中文句对数据集进行训练',
    '* Mixed 此文本嵌入模型支持中英双语的同质文本相似度计算，异质文本检索等功能，未来还会支持代码检索，ALL in one'
]

#Sentences are encoded by calling model.encode()
embeddings = model.encode(sentences)

#Print the embeddings
for sentence, embedding in zip(sentences, embeddings):
    print("Sentence:", sentence)
    print("Embedding:", embedding)
    print("")
```

M3E 系列的所有模型在设计的时候就考虑到完全兼容 sentence-transformers ，所以你可以通过**替换名称字符串**的方式在所有支持 sentence-transformers 的项目中**无缝**使用 M3E Models，比如 chroma, guidance, semantic-kernel 。

## 训练方案

M3E 使用 in-batch 负采样的对比学习的方式在句对数据集进行训练，为了保证 in-batch 负采样的效果，我们使用 A100 80G 来最大化 batch-size，并在共计 2200W+ 的句对数据集上训练了 1 epoch。训练脚本使用 uniem，您可以在这里查看具体细节。

## 特性

- 中文训练集，M3E 在大规模句对数据集上的训练，包含中文百科，金融，医疗，法律，新闻，学术等多个领域共计 2200W 句对样本，数据集详见 M3E 数据集
- 英文训练集，M3E 使用 MEDI 145W 英文三元组数据集进行训练，数据集详见 MEDI 数据集，此数据集由 instructor team 提供
- 指令数据集，M3E 使用了 300W + 的指令微调数据集，这使得 M3E 对文本编码的时候可以遵从指令，这部分的工作主要被启发于 instructor-embedding
- 基础模型，M3E 使用 hfl 实验室的 Roberta 系列模型进行训练，目前提供 small 和 base 两个版本，大家则需选用
- ALL IN ONE，M3E 旨在提供一个 ALL IN ONE 的文本嵌入模型，不仅支持同质句子相似度判断，还支持异质文本检索，你只需要一个模型就可以覆盖全部的应用场景，未来还会支持代码检索

## 参考链接：

```
https://mp.weixin.qq.com/s?__biz=MjM5ODkzMzMwMQ==&mid=2650437592&idx=2&sn=4ac30dda0c13ce8e99f9c569d9e72de0&chksm=becdf18289ba78943690b3b848b87339770d1a64414d0f818393e7d04c2a783b41d92522ef62&mpshare=1&scene=23&srcid=0828L29PWHn0K5PGKvIfXdo6&sharer_sharetime=1693180951120&sharer_shareid=58e5263b35a9b4aab08ac62984c9fc5a#rd
```

