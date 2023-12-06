import gradio as gr
from app_test import text_gen


def chat_once(xinput):
    xoutput = text_gen(xinput)
    return xoutput, ''


with gr.Blocks(analytics_enabled=False) as demo:
    # 输入控件
    cmp_input = gr.Textbox(interactive=True, label='输入')
    cmp_input_button = gr.Button('发送', )

    # 输出控件
    cmp_output = gr.Textbox(interactive=False, label='输出')

    # 按钮点击事件
    cmp_input_button.click(chat_once, [cmp_input], [cmp_output, cmp_input])

# 用gradio启动，但是这样queue就不正常，可能还是得用uvicorn启动
# demo.launch(server_name='0.0.0.0', server_port=7776, share=True, debug=True)
demo.launch(server_name='0.0.0.0', server_port=7776, debug=True)
