import re
# 正则表达式（Regular Expression）是一种用来匹配和操作字符串的强大工具，
# 它可以在文本中搜索、替换和提取符合特定模式的字符串。
#正则表达式的函数：
# 1,match函数示例
# match(pattern, string)：尝试从字符串的开头匹配指定的模式。如果匹配成功，返回一个匹配对象；否则返回None。
# pattern = r"hello"
# string_y = "hello world"
# string_n = "world hello"
# match_result = re.match(pattern, string_y)
# print("match_result: ", match_result.group())
# mistake_result = re.match(pattern, string_n)
# print("mistake_result: ", mistake_result)

# 2,search(pattern, string)：在字符串中搜索匹配指定的模式。如果匹配成功，返回一个匹配对象；否则返回None。
# 与match()不同的是，search()在整个字符串中搜索，而不仅仅是开头。
# search函数示例
# pattern = r"world"
# string = "hello world"
# mistake = r"jjjj"
# search_result = re.search(pattern, string)
# print("search_result: ", search_result.group())
# search_mistake = re.search(mistake, string)
# print("search_mistake: ", search_mistake)

# 3,findall(pattern, string)：在字符串中查找所有匹配指定的模式的子字符串，并返回一个包含所有匹配结果的列表。
# pattern = r"apple"
# text = "I like apple and apple pie."
# result = re.findall(pattern, text)
# print("Matches found:", result)

# 4,re.finditer(pattern, text)：返回一个迭代器，迭代器包含字符串中所有匹配的模式的匹配对象。
# pattern = r"apple"
# text = "I like apple and apple pie."
# result_iterator = re.finditer(pattern, text)
# for match in result_iterator:
#     print("Match found:", match.group())

# 5,split(pattern, string, maxsplit=0)：根据指定的模式对字符串进行拆分，并返回拆分后的子字符串列表。
# pattern = r"\s+"
# text = "apple orange   banana"
# result = re.split(pattern, text)
# print("Split result:", result)

# 6,sub(pattern, repl, string, count=0)：使用指定的替换字符串将字符串中所有匹配指定模式的子字符串替换掉。
# pattern = r"apple"
# replacement = "orange"
# text = "I like apple and apple pie."
# result = re.sub(pattern, replacement, text)
# print("Modified text:", result)

# 7,subn(pattern, repl, string, count=0)：与sub()函数类似，但返回一个元组，包含替换后的新字符串以及实际替换的次数。
# print(re.subn('ov', '~*' , 'movie tickets booking in online'))
# t = re.subn('ov', '~*' , 'movie tickets booking in online', flags = re.IGNORECASE)
# print(t)
# print(t[0])

# 8,compile(pattern)：编译指定的正则表达式模式，并返回一个正则表达式对象，用于在后续的匹配操作中使用。
# pattern = r"apple"
# text = "I like apple and apple pie."
# regex = re.compile(pattern)
# result = regex.findall(text)
# print("Matches found:", result)
# 正则表达式符号解释：
# .（点号）：匹配除换行符外的任意字符。
# pattern = r".at"  # 匹配任意字符后接"at"的字符串
# text = "cat, rat, hat"
# result = re.findall(pattern, text)
# print("Matches found:", result)

# # ^（脱字符）：匹配字符串的开头。
# pattern = r"^apple"  # 匹配以"apple"开头的字符串
# text = "apple pie is delicious"
# result = re.findall(pattern, text)
# print("Matches found:", result)
# #$（美元符号）：匹配字符串的结尾。
# pattern = r"ous$"  # 匹配以"pie"结尾的字符串
# text = "apple pie is delicious"
# result = re.findall(pattern, text)
# print("Matches found:", result)
# # *（星号）：匹配前面的表达式零次或多次。
# pattern = r"ab*c"  # 匹配a后面跟着零个或多个b，然后是c
# text = "ac abc abbc abbbc"
# result = re.findall(pattern, text)
# print("Matches found:", result)
# # +（加号）：匹配前面的表达式一次或多次。
# pattern = r"ab+c"  # 匹配a后面跟着至少一个b，然后是c
# text = "ac abc abbc abbbc"
# result = re.findall(pattern, text)
# print("Matches found:", result)
# #?（问号）：匹配前面的表达式零次或一次。
# pattern = r"ab?c"  # 匹配a后面跟着零个或一个b，然后是c
# text = "ac abc abbc abbbc"
# result = re.findall(pattern, text)
# print("Matches found:", result)
# # {n}：匹配前面的表达式恰好 n 次。
# pattern = r"ab{3}c"  # 匹配a后面跟着2个b，然后是c
# text = "ac abc abbc abbbc"
# result = re.findall(pattern, text)
# print("Matches found:", result)
# # {n,}：匹配前面的表达式至少 n 次。
# pattern = r"ab{2,}c"  # 匹配a后面跟着至少2个b，然后是c
# text = "ac abc abbc abbbc"
# result = re.findall(pattern, text)
# print("Matches found:", result)
# # {n,m}：匹配前面的表达式至少 n 次但不超过 m 次。
# pattern = r"ab{2,4}c"  # 匹配a后面跟着2到4个b，然后是c
# text = "ac abc abbc abbbc abbbbc"
# result = re.findall(pattern, text)
# print("Matches found:", result)
# # []（方括号）：匹配方括号中的任意一个字符。
# pattern = r"[aeiou]"  # 匹配任何一个小写元音字母
# text = "apple"
# result = re.findall(pattern, text)
# print("Matches found:", result)
# # |（竖线）：匹配竖线左右两边的表达式中的一个。
# pattern = r"apple|orange|jj"  # 匹配"apple"或"orange"
# text = "I like apples and oranges."
# result = re.findall(pattern, text)
# print("Matches found:", result)
# # ()（圆括号）：创建捕获组，用于分组匹配和提取匹配结果。
# pattern = r"(\d{4})-(\d{2})-(\d{2})"
# text = "Today's date is 2023-07-21."
# match = re.search(pattern, text)
# print(match.group())
# 1、匹配中文:[\u4e00-\u9fa5]
# pattern = r"[\u4e00-\u9fa5]+"
# text = "Today's date is 2023-07-21.你好"
# match = re.search(pattern, text)
# print(match.group())

# # \d：代表任意数字，就是阿拉伯数字0-9也可以表达为【0-9】
# pattern = r"[0-9]+"
# text = "The temperature today is 25°C."
# result = re.findall(pattern, text)
# print("Matches found:", result)
# # \D：与\d刚好相反，代表不是数字的。
# pattern = r"\D+"
# text = "The temperature today is 25°C."
# result = re.findall(pattern, text)
# print("Matches found:", result)
# # \w：代表字母，数字，下划线。就是a-z, A-Z, 0-9, _
# pattern = r"\w+"
# text = "Hello_world_123你好"
# result = re.findall(pattern, text)
# print("Matches found:", result)
# # \W：与\w正好相反，代表不是字母、数字以及下划线的。
# pattern = r"\W+"
# text = "Hello_world_123   "
# result = re.findall(pattern, text)
# print("Matches found:", result)
# # \n：代表一个换行。
# pattern = r"\n"
# text = "Hello\nWorld"
# result = re.findall(pattern, text)
# print("Matches found:", result)
# # \r：代表一个回车。
# pattern = r"\r"
# text = "Hello\rWorld"
# result = re.findall(pattern, text)
# print("Matches found:", result)
# # \f：代表换页。
# pattern = r"\f"
# text = "Hello\fWorld"
# result = re.findall(pattern, text)
# print("Matches found:", result)
# # \t：代表一个Tab。
# pattern = r"\t"
# text = "Hello\tWorld"
# result = re.findall(pattern, text)
# print("Matches found:", result)
# # \s：代表所有的空白字符， 也就是上面的：\n、 \r 、\t、 \f。
# pattern = r"\s+"
# text = "Hello\n\t World"
# result = re.findall(pattern, text)
# print("Matches found:", result)
# # \S：正好与\s相反， 代表所有不是空白的字符。
# pattern = r"\S+"
# text = "Hello\n\t World"
# result = re.findall(pattern, text)
# print("Matches found:", result)
# # \A：代表字符串的开始。
# pattern = r"\AHello"
# text = "Hello, World! Hello, Python!"
# result = re.findall(pattern, text)
# print("Matches found:", result)
# # \Z：代表字符串的结束。
# pattern = r"Python!\Z"
# text = "Hello, World! Hello, Python!"
# result = re.findall(pattern, text)
# print("Matches found:", result)
# # .：代表所有的单个字符， 除了\n \r
# pattern = r"t.m"
# text = "tom and tim went to the market"
# result = re.findall(pattern, text)
# print("Matches found:", result)
# # - \b：匹配单词的边界。
# pattern = r"\bapple\b"
# text = "I have an apple and a pineapple."
# result = re.findall(pattern, text)
# print("Matches found:", result)
# # - \B：匹配非单词的边界。
# pattern = r"\Bapple\B"
# text = "I have an and apineapple"
# result = re.findall(pattern, text)
# print("Matches found:", result)

# 零宽断言：
# - (?=...)：正向肯定预查，匹配后面紧跟的表达式。
# pattern = r"apple\d(?=pie)"
# text = "I like apple1pie and apple2 juice."
# result = re.search(pattern, text)
# print("Matches found:", result.group())
# - (?!...)：正向否定预查，匹配后面不紧跟的表达式。
# pattern = r"apple\d(?!pie)"
# text = "I like apple1 and apple2pie."
# result = re.search(pattern, text)
# print("Matches found:", result.group())


# # - (?<=...)：反向肯定预查，匹配前面紧靠的表达式。
# pattern = r"(?<=I like )apple\d"
# text = "I like apple1 and apple2 pie."
# result = re.search(pattern, text)
# print("Matches found:", result.group())
# # - (?<!...)：反向否定预查，匹配前面不紧靠的表达式。
# pattern = r"(?<!I like )apple\d"
# text = "I like apple1 and apple2 pie."
# result = re.findall(pattern, text)
# print("Matches found:", result)


# 非贪婪匹配（非默认模式）：
# 默认情况下，正则表达式是贪婪匹配的，即尽可能多地匹配。但可以通过在重复符号后添加?来实现非贪婪匹配，即尽可能少地匹配。
# text = "I love python programming. Python is fun!"
# pattern_greedy = r"p.*n"  # 贪婪匹配
# result_greedy = re.findall(pattern_greedy, text)
# print("Greedy match:", result_greedy)
# pattern_non_greedy = r"p.*?n"  # 非贪婪匹配
# result_non_greedy = re.findall(pattern_non_greedy, text)
# print("Non-greedy match:", result_non_greedy)

#re模块中，re.group(1)用于访问匹配对象中特定索引的捕获组的内容。捕获组是使用圆括号来定义的子正则表达式，
# 它允许在匹配过程中提取指定的文本片段。re.group(1)返回匹配对象中第一个捕获组的内容，索引从1开始。
# text = "I love python programming. Python is fun!"
# result = re.search(r'lo(\D+)', text)
# print(result.group())
# print(result.group())


# ^[1-9]d*$　 　 //匹配正整数
# ^-[1-9]d*$　 //匹配负整数
# ^-?[1-9]d*$　　 //匹配整数
# ^[1-9]d*|0$　 //匹配非负整数（正整数 + 0）
# ^-[1-9]d*|0$　　 //匹配非正整数（负整数 + 0）
# ^[1-9]d*.d*|0.d*[1-9]d*$　　 //匹配正浮点数
# ^-([1-9]d*.d*|0.d*[1-9]d*)$　 //匹配负浮点数
# ^-?([1-9]d*.d*|0.d*[1-9]d*|0?.0+|0)$　 //匹配浮点数
# ^[1-9]d*.d*|0.d*[1-9]d*|0?.0+|0$　　 //匹配非负浮点数（正浮点数 + 0）
# ^(-([1-9]d*.d*|0.d*[1-9]d*))|0?.0+|0$　　//匹配非正浮点数（负浮点数 + 0）





















