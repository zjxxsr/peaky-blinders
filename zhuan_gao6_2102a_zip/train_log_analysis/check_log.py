import sys
import re
import matplotlib.pyplot as plt
import traceback
import numpy as np

xregex_step = re.compile(r'at step (\d+)\:')
xregex_loss = re.compile(r' loss \= ([0-9\-\.e]+)')
xregex_lr = re.compile(r' learning_rate \= ([0-9\-\.e]+)')
xregex_eval_loss = re.compile(r' eval_loss \= ([0-9\-\.e]+)')
xregex_eval_acc = re.compile(r' eval_accuracy \= ([0-9\-\.e]+)')

if '__main__' == __name__:
    # 从命令行拿到日志路径
    argc = len(sys.argv)
    if argc <= 1:
        print('Please provide the log path!')
        sys.exit(1)
    log_path = sys.argv[1]

    xmax_step = 0
    with open(log_path, 'r',encoding='utf8') as xfin:
        while True:
            xline = xfin.readline()
            if not xline:
                break
            if '\r\n' == xline[-2:]:
                xline = xline[:-2]
            else:
                xline = xline[:-1]
            xm = xregex_step.search(xline)
            if xm is not None:
                try:
                    xstep = 0
                    xstep = int(xm[1])
                except Exception as ex:
                    print(traceback.format_exc())
                if xstep > xmax_step:
                    xmax_step = xstep
    print('max step:', xmax_step)

    # 读取日志
    loss_np = np.zeros((xmax_step, ), dtype=np.float32)
    lr_np = np.zeros((xmax_step,), dtype=np.float32)
    eval_loss_np = np.zeros((xmax_step, ), dtype=np.float32)
    eval_acc_np = np.zeros((xmax_step, ), dtype=np.float32)
    with open(log_path, 'r',encoding='utf8') as xfin:
        while True:
            xline = xfin.readline()
            if not xline:
                break
            if '\r\n' == xline[-2:]:
                xline = xline[:-2]
            else:
                xline = xline[:-1]

            xm = xregex_step.search(xline)
            if xm is not None:
                try:
                    xstep = 0
                    xstep = int(xm[1])
                except Exception as ex:
                    print(traceback.format_exc())
            if not xstep:
                continue
            xstep -= 1

            xm = xregex_loss.search(xline)
            if xm is not None:
                try:
                    xval = 0.0
                    xval = float(xm[1])
                except Exception as ex:
                    print(traceback.format_exc())
                loss_np[xstep] = xval

            xm = xregex_lr.search(xline)
            if xm is not None:
                try:
                    xval = 0.0
                    xval = float(xm[1])
                except Exception as ex:
                    print(traceback.format_exc())
                lr_np[xstep] = xval

            xm = xregex_eval_loss.search(xline)
            if xm is not None:
                try:
                    xval = 0.0
                    xval = float(xm[1])
                except Exception as ex:
                    print(traceback.format_exc())
                eval_loss_np[xstep] = xval

            xm = xregex_eval_acc.search(xline)
            if xm is not None:
                try:
                    xval = 0.0
                    xval = float(xm[1])
                except Exception as ex:
                    print(traceback.format_exc())
                eval_acc_np[xstep] = xval

    spr = 1
    spc = 3
    spn = 0

    spn += 1
    plt.subplot(spr, spc, spn)
    plt.plot(loss_np, label='loss')
    plt.plot(eval_loss_np, label='eval_loss')
    plt.legend()

    spn += 1
    plt.subplot(spr, spc, spn)
    plt.plot(eval_acc_np, label='eval_acc')
    plt.legend()

    spn += 1
    plt.subplot(spr, spc, spn)
    plt.plot(lr_np, label='lr')
    plt.legend()

    print('Check and close the plotting window to continue ..')
    plt.show()

    print('All over')
