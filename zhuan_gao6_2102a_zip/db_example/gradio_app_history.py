import time
import gradio as gr
from app_test import text_gen
from util import uuid, merge_dialog_in_and_out, translate_ns
from http.cookies import SimpleCookie
from util_mongo import (
    enqueue,
    get_sorted_by_key,
)
from util_mysql import (
    enqueue as enqueue_mysql,
    get_sorted_by_key as get_sorted_by_key_mysql
)
from common import MONGODB_NAME, VALUE, KEY, IO_PREFIX
import pymongo as pm
import pymysql
import os
import redis

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

    # 清空动态响应
    rdb.delete('chat_cache_' + username)

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


def show_text_out_cache(username):
    if username is None:
        return ''

    cache = rdb.get('chat_cache_' + username)
    if cache is None:
        return ''
    cache = cache.decode('utf8')
    return cache


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

    # 按钮点击事件
    xinput_button.click(chat_once, [cmp_username_state, xinput], [cmp_chatbot, xinput], queue=False)

    # 输出动态响应
    cmp_start_btn.click(show_text_out_cache, cmp_username_state, cmp_text_out_cache, every=0.1, )

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
