# coding:utf-8
import ahocorasick
import os

# 处理完后的疾病对应的症状
input_path_noreview= r'D:\生涯项目文件\NLP53.0\ai13bj\doctor_offline\structured\reviewed'
# 疾病文件组成一个列表
csv_list = os.listdir(input_path_noreview)
# 定义一个空的列表，存储疾病的症状
all_list = []
# 比那里每一个疾病的文件
for csv in csv_list:
    # 打开每一个疾病的文件
    with open(os.path.join(input_path_noreview, csv), 'r',encoding='utf-8') as fr:
        # 读取整个文件按行杜
        all = fr.readlines()
        # 读取每一个文件的每一行
        for i in all:
            i = i.replace('\n','')
            # 判断行的长度是否为0
            if len(i)>0:
                # 列表添加每一个症状
                all_list.append(i)
# all_list = all_list
# print('keylist',all_list)
# for i in all_list:
#     print(i)


def make_AC(AC, word_set):
    for word in word_set:
        AC.add_word(word, word)
    return AC

# 自动机函数
def test_ahocorasick(snetence):
    '''
    ahocosick：自动机的意思
    可实现自动批量匹配字符串的作用，即可一次返回该条字符串中命中的所有关键词
    '''
    # key_list = ["苹果", "香蕉", "梨", "橙子", "柚子", "火龙果", "柿子", "猕猴挑"]
    # key_list = ["血糖值升高", '餐后血糖高', '眼球内陷', '下颌角外翻', '外斜A征', '双眼向上凝视', '外斜V征', '内斜A征']
    key_list = all_list
    AC_KEY = ahocorasick.Automaton()

    AC_KEY = make_AC(AC_KEY, set(key_list))

    AC_KEY.make_automaton()

    # test_str_list = ["我最喜欢吃的水果有：苹果、梨和香蕉", "我也喜欢吃香蕉，但是我不喜欢吃梨"]
    test_str_list = [snetence]
    for content in test_str_list:
        name_list = set()
        for item in AC_KEY.iter(content):  # 将AC_KEY中的每一项与content内容作对比，若匹配则返回
            name_list.add(item[1])
        name_list = list(name_list)
        if len(name_list) > 0:
            # print("".join(name_list))
            return "".join(name_list)

        else:
            return snetence


# print(test_ahocorasick('我今天很头痛'))
# print(test_ahocorasick('我今天不舒服眼球内陷'))
# print(test_ahocorasick('我今天不舒服，眼球'))
# print(test_ahocorasick(''))