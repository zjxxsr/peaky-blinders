import json
def change(data):
    text=[]
    label=[]
    with open(data,"r",encoding="utf8") as file:
        for i in file.readlines():
            data_json=json.loads(i)
            text_values=data_json["text"]
            for i in text_values:
                text.append(i)
            label_values=data_json["label"]
            for j in label_values:
                label.append(j)
    result=list(zip(text,label))
    with open("validate_change.txt","w",encoding="utf8") as file:
        for i in result:
            file.write(f"{i[0]}\t{i[1]}\n")
    with open("validate_change.txt","r",encoding="utf8") as file:
        f=file.read()
    return f
if __name__=="__main__":
    data_json=change("validate.txt")
    print(data_json)