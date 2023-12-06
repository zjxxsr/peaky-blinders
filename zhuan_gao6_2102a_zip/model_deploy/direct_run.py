from modelscope.pipelines import pipeline
from modelscope.utils.constant import Tasks
text_generation_zh = pipeline(Tasks.text_generation, model='damo/nlp_gpt3_text-generation_chinese-base')
result_zh = text_generation_zh("您好！")
print(result_zh['text'])
