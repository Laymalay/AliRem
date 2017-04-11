#!/usr/bin/python
# -*- coding: UTF-8 -*-
import threading
import time
from blessings import Terminal
import colorama


def show_progress(task, total_size, get_now_size):
    PROGRESS_SIZE = 100
    worker = threading.Thread(target=task)
    colorama.init() # replace ANSI escapes with Win32 calls in stdout/stderr
    t = Terminal()
    worker.start()

    while worker.isAlive():
        time.sleep(0.1)
        try:
            now_size = get_now_size()
        except Exception:
            return

        progress = int((float(now_size) / (total_size + 1)) * PROGRESS_SIZE)
        a = t.red
        if progress > 20:
            a = t.red
        if progress > 50:
            a = t.yellow
        if progress > 80:
            a = t.green


        print a("{}{}|{}".format("#" * progress, " " * (PROGRESS_SIZE - progress), "\033[F"))
    print t.green("{}|{}".format("#" * 100, "\033[F"))
    print
