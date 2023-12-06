python3 daemon.py >/daemon.log 2>&1 &
python3 app.py >/app.log 2>&1 &
python3 gradio_cookie_history.py