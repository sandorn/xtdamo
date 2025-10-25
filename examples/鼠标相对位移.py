# !/usr/bin/env python
"""
==============================================================
Description  : 头部注释
Develop      : VSCode
Author       : sandorn sandorn@live.cn
Date         : 2025-05-30 11:35:88
LastEditTime : 2025-05-30 16:09:24
FilePath     : /CODE/xjLib/xt_damo/鼠标相对位移.py
Github       : https://github.com/sandorn/home
==============================================================
# 相对位移`dm.MoveR`测试

- 相对位移的误差问题
"""

from __future__ import annotations

from xtlog import mylog

from xtdamo.damo import DmExcute

dm = DmExcute()
mylog.info(f'Mouse position: {dm.position}')  # 当前鼠标位置

xy_ls = [[1109, 545], [545, 1109], [1109, 545], [545, 1109], [1109, 545], [545, 1109]]
x_ls = []
for i in range(20):
    # 简化的停止检查（可以按Ctrl+C停止）
    try:
        xy_i = i % len(xy_ls)
        xy_v = xy_ls[xy_i]
        dm.MoveTo(*xy_v)

        x_i = dm.position[0]
        x_ls.append(x_i)
        delta_x = 0 if len(x_ls) < 2 else x_ls[-1] - x_ls[-2]
        mylog.info(f'--- {i} --- \t Mouse position: {x_i}, \t target_x: {xy_v}, \t delta_x: {delta_x}')

        import time

        time.sleep(0.2)
    except KeyboardInterrupt:
        mylog.info('*** 暂停!')
        break
