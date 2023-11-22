import json
json_objects=[]
with open("medical.json","r",encoding="utf8") as file:
    for i in file.readlines():
        json_object=json.loads(i)
        json_objects.append(json_object)

key_list=[]
for i in json_objects:
    for j in i.keys():
        key_list.append(j)

key_list=list(set(key_list))
print(key_list)
print(len(key_list))



