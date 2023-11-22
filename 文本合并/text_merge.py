import pickle

def merge_and_save(*file_paths, output_file="merged_text.txt"):
    merged_data = ""
    for file_path in file_paths:
        with open(file_path, "r", encoding="utf-8") as file:
            merged_data += file.read()

    with open(output_file, "wb") as output:
        pickle.dump(merged_data, output)

    with open(output_file, "rb") as input_file:
        return pickle.load(input_file, encoding="utf-8")

if __name__ == "__main__":
    merged_text = merge_and_save("text1.txt", "text2.txt", "text3.txt", "text4.txt", "text5.txt")
    print(merged_text)