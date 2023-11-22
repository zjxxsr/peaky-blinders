import json
texts=[]
labels=[]
with open('validate.txt', encoding='utf8') as f:
    data=f.readlines()
    for i in data:
        data_j=json.loads(i)
        text_values=data_j['text']
        for line in text_values:
                texts.append(line)
        label_values=data_j['label']
        for i in label_values:
            labels.append(i)
result=zip(texts,labels)
results=list(result)

with open("output3.txt","w",encoding="utf8") as file:
    for i in results:
        file.write(f"{i[0]}\t{i[1]}\n")