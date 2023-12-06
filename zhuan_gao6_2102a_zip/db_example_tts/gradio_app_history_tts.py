import threading
import time
import gradio as gr
from app_test import text_gen
from util import uuid, merge_dialog_in_and_out, translate_ns, compose_wav_header, get_pos_of_first_punct
from http.cookies import SimpleCookie
from util_mongo import (
    enqueue,
    get_sorted_by_key,
)
from util_mysql import (
    enqueue as enqueue_mysql,
    get_sorted_by_key as get_sorted_by_key_mysql
)
from common import MONGODB_NAME, VALUE, KEY, IO_PREFIX, RATE
import pymongo as pm
import pymysql
import os
import redis
import base64
from tts_ws_python3_demo_mod import XunfeiTts

# 连接Mongodb
mongo = pm.MongoClient(os.environ.get('MONGO_HOST', '127.0.0.1'), int(os.environ.get('MONGO_PORT', 27017)), serverSelectionTimeoutMS=3000)
mdb = mongo[MONGODB_NAME]

# 连接redis
rdb = redis.Redis(os.environ.get('REDIS_HOST', '127.0.0.1'), int(os.environ.get('REDIS_PORT', 6379)), 0)

# 连接mysql
xdb_args = dict(
    host='127.0.0.1',
    port=3306,
    user='root',
    password='rootA1-',
    database='db_bawei',
    charset='utf8'
)
mydb = pymysql.connect(**xdb_args)


def embed_user_id_in_state_comp(request: gr.Request):
    """
    页面加载的事件handler

    从HTTP request中获取cookie来确定用户名，如果没有则生成一个
    :param request: HTTP request JSON
    :return: 将用户名发送给浏览器和存放用户名的组件
    """
    xuuid = uuid()

    #从cookie中获取username
    username = None
    try:
        cookie_str = request.headers.cookie
        print('cookie_str:', cookie_str)
        cookie = SimpleCookie()
        cookie.load(cookie_str)
        username = cookie.get('username', None)
        print('user:', username)
        username = username.value
    except Exception:
        try:
            username = request.cookies['username']
        except Exception:
            pass

    # 获取不到，新建一个username
    if username is None:
        print('new user!')
        username = f'u{xuuid}'

    # print username
    print('user:', username)

    log = update_chat_history(username)

    return username, username, username, log


def chat_once(username, xinput):
    if username is None:
        return [], ''

    # 输入 入库
    ts = time.time_ns()
    enqueue(mdb, 'dialog_in', username, ts, {
        VALUE: xinput,
        'io': 'i',
    })

    # 得到输出
    xoutput = text_gen(xinput, username)

    # 不以标点结尾的动态响应，最后的部分要在这里进行TTS
    # 动态响应内容
    cache = rdb.get('chat_cache_' + username)
    if cache is None:
        cache = b''
    cache = cache.decode('utf8')
    xlen = len(cache)
    # 目前的切分位置
    xstart = rdb.get('start_' + username)
    if xstart is None:
        xstart = 0
    else:
        xstart = int(xstart)
    # 切出最后
    if xstart < xlen - 1:
        print(']]]]----]]]]', xstart, )
        xlast = cache[xstart:]

        def worker():
            xunfei_obj = XunfeiTts(username, rdb, 'audio_' + username)
            xunfei_obj.tts(xlast)

        threading.Thread(target=worker).start()

    # 清空动态响应
    rdb.delete('chat_cache_' + username)
    rdb.delete('start_' + username)

    # 输出 入库
    ts = time.time_ns()
    enqueue_mysql(mydb, 'dialog_out', username, ts, {
        VALUE: xoutput,
        'io': 'o',
    })
    log = update_chat_history(username)
    return log, ''


def update_chat_history(username):
    """
    刷新聊天记录的handler

    :param username:
    :return: list of list
    """
    if username is None:
        return []

    rows_in = get_sorted_by_key(mdb, 'dialog_in', username, limit=5, is_keep_others=False)  # DESC
    rows_out = get_sorted_by_key_mysql(mydb, 'dialog_out', username, limit=5, is_keep_others=False)  # DESC
    rows = merge_dialog_in_and_out(rows_in, rows_out)  # DESC
    rows = rows[::-1]  # ASC

    if not len(rows):
        log = []
    else:
        log = []
        pair = [None, None]
        for row in rows:
            text = row[VALUE]
            timestamp = row[KEY]
            dt_str = translate_ns(timestamp)
            xstr = IO_PREFIX.get(row["io"], '?') + ': '
            xstr += f'[ {dt_str} ] '

            xstr += text

            if 'i' == row['io']:
                if pair[0] is not None or pair[1] is not None:
                    log.append(pair)
                    pair = [xstr, None]
                    continue
                pair[0] = xstr
            elif 'o' == row['io']:
                if pair[1] is not None:
                    log.append(pair)
                    pair = [None, xstr]
                    continue
                pair[1] = xstr
        log.append(pair)

    return log


def do_the_init():
    """
        点击”开始聊天“的事件的handler
        :return: 隐藏”开始聊天“，显示其他组件。
    """
    return (
        gr.update(visible=False),
        *([gr.update(visible=True)] * 3),
    )


def show_text_out_cache_and_play_tts(username):
    if username is None:
        return '', ''

    # 文本动态响应
    cache = rdb.get('chat_cache_' + username)
    if cache is None:
        cache = b''
    cache = cache.decode('utf8')
    # 截取
    xstart = rdb.get('start_' + username)
    if xstart is None:
        xstart = 0
    else:
        xstart = int(xstart)
    sub_cache_all = cache[xstart:]
    xpos = get_pos_of_first_punct(sub_cache_all)
    if xpos is not None:
        print(']]]]', xstart, xpos)
        sub_cache = sub_cache_all[:xpos]
        xstart += xpos + 1
        rdb.set('start_' + username, str(xstart))

        # TTS
        def worker():
            xunfei_obj = XunfeiTts(username, rdb, 'audio_' + username)
            xunfei_obj.tts(sub_cache)

        threading.Thread(target=worker).start()

    # 语音连续播放
    audio = rdb.rpop('audio_' + username)
    if audio is None:
        return cache, ''

    # 加wave头
    xlen = len(audio)
    header = compose_wav_header(xlen, 1, 16, RATE)
    wav = header + audio

    # base64编码
    wav_b64 = base64.b64encode(wav).decode('ascii')
    html = f'<audio src="data:audio/wav;base64,{wav_b64}" controls></audio>'

    return cache, html


# 用户名写入cookie的JS
js_username2cookie = """
    async () => {{
            setTimeout(() => {{
                var xnew = document.querySelector('#username.prose').innerHTML;
                //console.log('username', xnew)
                if ('' == xnew) {
                    return;
                }
                document.cookie = 'username=' + xnew + '; max-age=' + 3600*24*30*6;
            }}, 1);
        }}
"""

# TTS播放配套的JS
js_code = """
    async () => {{
            setTimeout(function(){

                // new audio
                var xnew = document.querySelector('#audio_out.prose').innerHTML;
                if ('' == xnew) {
                    return;
                }
                window.audio_id = window.audio_id || 0;
                window.audio_id += 1;
                console.log(audio_id, new Date(), 'xnew', xnew.length)

                // append
                var room = document.querySelector('#audio_room.prose');
                var div = document.createElement('div');
                div.id = 'my_audio_' + audio_id;
                room.append(div);
                console.log(audio_id, new Date(), 'appended');

                // start ened event and trigger playing if needed
                div.innerHTML = xnew;
                var xnew_audio = div.querySelector('audio')
                if (!xnew_audio) {
                    console.log(audio_id, new Date(), 'new audio in div not found');
                    return;
                }
                xnew_audio.addEventListener('ended', function(){
                    var _this = this;

                    // remove this
                    setTimeout(function(){
                        _this.remove();
                        console.log(audio_id, new Date(), 'removed')
                    }, 100);
                    console.log(audio_id, new Date(), 'register this.remove');

                    // play next
                    var slot_after = div.nextElementSibling;
                    if (!slot_after) {
                        console.log(audio_id, new Date(), 'no slot_after');
                        window.is_need_manual = true;
                        return;
                    }
                    var next_audio = slot_after.querySelector('audio');
                    if (!next_audio) {
                        console.log(audio_id, new Date(), 'no next_audio');
                        window.is_need_manual = true;
                        return;
                    }
                    window.is_need_manual = false;
                    console.log(audio_id, new Date(), 'play next_audio');
                    next_audio.play();

                }, false);
                console.log(audio_id, new Date(), 'ended event registered');

                if (1 == audio_id || window.is_need_manual) {
                    console.log(audio_id, new Date(), 'manually play');
                    window.is_need_manual = false;
                    xnew_audio.play();
                }

            }, 1);
        }}
"""

with gr.Blocks(analytics_enabled=False) as demo:
    # 用户名
    cmp_username_state = gr.State()
    cmp_username_html = gr.HTML(visible=False, elem_id='username')
    cmp_username_display = gr.Textbox(interactive=False, label='用户名')

    # 启动按钮
    cmp_start_btn = gr.Button('开始聊天')

    # 聊天历史
    cmp_chatbot = gr.Chatbot().style(height=350)

    # 动态响应输出控件
    cmp_text_out_cache = gr.Textbox(visible=False, interactive=False, label='动态响应')

    # 输入控件
    xinput = gr.Textbox(visible=False, interactive=True, label='输入')
    xinput_button = gr.Button('发送', visible=False, )

    # 语音播放
    cmp_play_audio = gr.HTML(elem_id='audio_out')
    # cmp_play_audio.visible = False
    cmp_play_audio_room = gr.HTML(elem_id='audio_room')
    # cmp_play_audio_room.visible = False

    # 按钮点击事件
    xinput_button.click(chat_once, [cmp_username_state, xinput], [cmp_chatbot, xinput], queue=False)

    # 激活：输出动态响应 和 语音连续播放
    cmp_start_btn.click(show_text_out_cache_and_play_tts, cmp_username_state, [
        cmp_text_out_cache,
        cmp_play_audio,
    ], every=0.1, )
    # 语音连续播放
    cmp_play_audio.change(None, None, None, _js=js_code, queue=False)

    # 加载时获取或设置cookie
    demo.load(embed_user_id_in_state_comp, None, [
        cmp_username_state,
        cmp_username_display,
        cmp_username_html,
        cmp_chatbot,
    ], queue=False)
    # cmp_username_html发生变化时，触发JS，把生成的username放入页面cookie
    cmp_username_html.change(None, None, None, _js=js_username2cookie, queue=False)

    # 启动
    cmp_start_btn.click(do_the_init, None, [
        cmp_start_btn,
        cmp_text_out_cache,
        xinput,
        xinput_button,
    ], queue=False)

# 使用queue
demo.queue(
    concurrency_count=10,
    status_update_rate='auto',
    # status_update_rate=0.02,
)

# 用gradio启动，但是这样queue就不正常，可能还是得用uvicorn启动
# demo.launch(server_name='0.0.0.0', server_port=7776, share=True, debug=True)
demo.launch(server_name='0.0.0.0', server_port=7776, debug=True)
