# !/usr/bin/env python
"""
==============================================================
Description  : 头部注释
Develop      : VSCode
Author       : sandorn sandorn@live.cn
Date         : 2025-05-30 11:35:10
LastEditTime : 2025-06-06 10:22:25
FilePath     : /CODE/xjLib/xt_damo/像素颜色捕捉.py
Github       : https://github.com/sandorn/home
==============================================================
"""

from __future__ import annotations

import time
from datetime import datetime

from xtdamo.damo import DmExcute
from xtdamo.time_utils import TimeTracker

dm = DmExcute()


def conv_to_rgb(color):
    RGB_str = [color[:2], color[2:-2], color[-2:]]
    return [int(i, 16) for i in RGB_str]


# 创建时间跟踪器，10秒超时
time_tracker = TimeTracker(10)

while time_tracker.during():  # 10s内捕捉鼠标当前位置的颜色
    time.sleep(0.1)
    # 简化的停止检查（可以按Ctrl+C停止）
    try:
        x, y = dm.position
        color = dm.GetColor(x, y)

        # 获取当前时间
        current_time = datetime.now().strftime('%H:%M:%S.%f')[:-3]
        print(f'{current_time},\t {x}:{y},\t color:{color}, \t 鼠标位置颜色RGB值:{conv_to_rgb(color)}')
    except KeyboardInterrupt:
        print('--- stopped!')
        break
