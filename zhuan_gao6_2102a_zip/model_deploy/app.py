from flask import Flask, url_for, request

app = Flask(__name__)

# from modelscope.pipelines import pipeline
# from modelscope.utils.constant import Tasks
# text_generation_zh = pipeline(Tasks.text_generation, model='damo/nlp_gpt3_text-generation_chinese-base')

fake_chat_dict = {
    0: '十全十美！',
    1: '一把钢枪交给我！',
    2: '二话不说为祖国！',
    3: '三山五岳任我走。',
    4: '四海为家。',
    5: '五福同寿。',
    6: '六六大顺！',
    7: '97香港回归。',
    8: '零八奥运。',
    9: '九九归一。',
}


def text_generation_zh(xinput):
    xlen = len(xinput)
    xoutput = f'您说了{xlen}个字符。（{xinput[:5]}……）' + fake_chat_dict[xlen % 10]
    return {
        'text': xoutput,
    }


@app.route("/api", methods=['POST'])
def do_infer():
    req_json = request.get_json(force=True)  # 请求json
    xinput = req_json['input']
    print('input:', xinput)
    xoutput = text_generation_zh(xinput)
    print('output', xoutput)
    xoutput = xoutput['text']

    res_json = dict()
    res_json['input'] = xinput
    res_json['output'] = xoutput
    return res_json


if '__main__' == __name__:
    # 启动方式1： 启动命令
    # flask run --host=0.0.0.0 --port=7777

    # 启动方式2： 在这里启动
    # https://www.cnblogs.com/chaojiyingxiong/p/14988069.html
    app.run('0.0.0.0', 7777)
