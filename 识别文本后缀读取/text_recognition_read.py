import json
import pandas as pd
import os
import pandas as pd



def data_read(*data):
    json_objects = []
    for data_list in data:
        _, file_extension = os.path.splitext(data_list)
        if file_extension == ".csv":
            data_csv = pd.read_csv(data_list, header=None, on_bad_lines="skip")

        elif file_extension==".json":
            with open(data_list, "r", encoding="utf8") as file:
                for i in file.readlines():
                    json_object=json.loads(i)
                    json_objects.append(json_object)
        elif file_extension==".txt":
            with open(data_list, "r", encoding="utf8") as file:
                data_text=file.read()
        elif file_extension == ".xlsx":
            data_xlsx=pd.read_excel(data_list,header=None)

    return data_csv,json_objects,data_text,data_xlsx


if __name__ == "__main__":
    data_csv,data_json,data_text,data_xlsl= data_read("数字.csv", "medical.json","sentence.txt","test.xlsx")
    print(data_csv,data_json,data_text,data_xlsl)




