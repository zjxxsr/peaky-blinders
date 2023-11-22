import os
import json
import pandas as pd
class DataRead:
    def __init__(self, *data):
        self.dataframes = {}
        self.read_data(*data)

    def read_data(self, *files):
        for file in files:
            self.read_file(file)

    def read_file(self, file):
        _, file_extension = os.path.splitext(file)
        file_extension = file_extension.lower()

        if file_extension in (".csv", ".json"):
            # 只处理 .csv 和 .json 文件
            if file_extension == ".csv":
                data = pd.read_csv(file, header=None,encoding="utf8", on_bad_lines="skip")
            elif file_extension == ".json":
                with open(file, 'r',encoding="utf8") as json_file:
                    data = json.load(json_file)
                    data = pd.json_normalize(data)

            self.dataframes[file] = data
            print(f"Reading file: {file}")
        else:
            print(f"Skipping unsupported file: {file}")

if __name__ == "__main__":
    data_reader = DataRead("数字.csv","medical.json")

