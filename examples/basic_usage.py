# !/usr/bin/env python
"""
xtdamo 基本使用示例
"""

from __future__ import annotations

from xtdamo import DmExcute


def main():
    """基本使用示例"""
    try:
        # 初始化大漠插件
        dm = DmExcute()
        print(f'大漠插件版本: {dm.ver()}')
        print(f'插件ID: {dm.GetID()}')

        # 获取当前鼠标位置
        x, y = dm.position
        print(f'当前鼠标位置: ({x}, {y})')

        # 移动鼠标
        dm.MoveTo(100, 100)
        print('鼠标已移动到 (100, 100)')

        # 点击操作
        dm.safe_click(200, 200)
        print('已点击 (200, 200)')

        # 键盘操作
        dm.Key.KeyPressStr('A')
        print('已按下 A 键')

    except Exception as e:
        print(f'发生错误: {e}')


if __name__ == '__main__':
    main()
