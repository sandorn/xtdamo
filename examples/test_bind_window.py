# !/usr/bin/env python3
"""测试窗口绑定和文本输入示例

这是一个简化的示例程序，演示如何：
1. 启动或查找记事本窗口
2. 使用前台模式绑定窗口
3. 向记事本输入示例文本
4. 执行基本的鼠标和键盘操作

使用方法:
    python test_bind_window.py

注意事项:
    - 使用前台绑定模式（gdi），不需要管理员权限
    - 如果记事本未运行，程序会自动启动
    - 测试完成后会保持记事本打开，可手动关闭

作者: sandorn <sandorn@live.cn>
版本: 0.2.0
日期: 2025-10-25
==============================================================
"""

from __future__ import annotations

import subprocess  # noqa: S404
import sys
from time import sleep

from xtdamo import DmExcute, __version__
from xtdamo.time_utils import VirtualKeys

dm = DmExcute()


def find_or_launch_notepad() -> int:
    """查找或启动记事本窗口

    Returns:
        int: 窗口句柄，0 表示失败
    """
    print('\n' + '=' * 60)
    print('步骤 1: 查找或启动记事本')
    print('=' * 60)

    # 尝试查找已存在的记事本窗口
    hwnd = dm.FindWindow('Notepad', '')

    if hwnd != 0:
        print(f'✓ 找到已存在的记事本窗口: {hwnd}')
        return hwnd

    # 如果没找到，启动记事本
    print('→ 记事本未运行，正在启动...')
    try:
        subprocess.Popen(['notepad.exe'])  # noqa: S607
        sleep(1.5)  # 等待记事本启动

        # 再次查找窗口
        hwnd = dm.FindWindow('Notepad', '')
        if hwnd != 0:
            print(f'✓ 记事本启动成功，窗口句柄: {hwnd}')
            return hwnd
        else:
            print('✗ 启动记事本后仍未找到窗口')
            return 0
    except Exception as e:
        print(f'✗ 启动记事本失败: {e}')
        return 0


def test_bind_and_input():
    """测试窗口绑定和文本输入"""
    print('\n' + '=' * 60)
    print('xtdamo v0.2.0 - 窗口绑定与文本输入示例')
    print('=' * 60)

    # 初始化大漠插件
    print('\n→ 初始化 xtdamo...')

    print('✓ xtdamo 初始化成功')
    print(f'  - 库版本: {__version__}')
    print(f'  - 插件版本: {dm.ver()}')

    # 查找或启动记事本
    hwnd = find_or_launch_notepad()
    if hwnd == 0:
        print('\n✗ 测试失败：无法获取记事本窗口')
        return False

    # 绑定窗口（前台模式）
    print('\n' + '=' * 60)
    print('步骤 2: 绑定窗口（前台模式）')
    print('=' * 60)

    try:
        # 使用前台绑定模式（不需要管理员权限）
        dm.绑定窗口(
            hwnd,
            display='gdi',  # 前台显示模式
            mouse='normal',  # 前台鼠标模式
            keypad='normal',  # 前台键盘模式
            mode=0,  # 前台绑定模式
        )
        print('✓ 窗口绑定成功')
        print('  - 显示模式: gdi (前台)')
        print('  - 鼠标模式: normal (前台)')
        print('  - 键盘模式: normal (前台)')
        print('  - 绑定模式: 0 (前台)')
    except Exception as e:
        print(f'✗ 窗口绑定失败: {e}')
        return False

    # 激活窗口（确保记事本在前台）
    print('\n→ 激活记事本窗口...')
    dm.SetWindowState(hwnd, 1)  # 显示窗口
    sleep(0.5)

    # 输入示例文本
    print('\n' + '=' * 60)
    print('步骤 3: 输入示例文本')
    print('=' * 60)

    sample_text = """xtdamo v0.2.0 测试示例
========================

这是一个自动化输入的示例文本。

核心特性:
1. 分层架构设计
2. 智能方法路由
3. 完整的参数验证
4. 友好的错误处理

鼠标操作示例:
- 移动: MoveTo(x, y)
- 点击: LeftClick()
- 安全点击: safe_click(x, y)

键盘操作示例:
- 按键: KeyPress(vk_code)
- 输入文本: KeyPressStr(text)
- 组合键: KeyDown + KeyPress + KeyUp

测试完成！
"""

    try:
        print('→ 开始输入文本...')

        # 逐行输入，模拟真实的打字过程
        lines = sample_text.split('\n')
        for i, line in enumerate(lines, 1):
            if line.strip():  # 跳过空行的输出消息
                print(f'  [{i}/{len(lines)}] 输入: {line[:50]}{"..." if len(line) > 50 else ""}')
            dm.KeyPressStr(line, 30)  # 每个字符间隔30ms
            dm.KeyPress(VirtualKeys.ENTER)  # 回车换行
            sleep(0.1)  # 每行之间稍微停顿

        print(f'✓ 文本输入完成，共 {len(lines)} 行')

    except Exception as e:
        print(f'✗ 文本输入失败: {e}')
        return False

    # 演示其他操作
    print('\n' + '=' * 60)
    print('步骤 4: 演示其他操作')
    print('=' * 60)

    try:
        # 全选文本 (Ctrl+A)
        print('→ 执行全选操作 (Ctrl+A)...')
        sleep(0.5)
        dm.Key.KeyDown(VirtualKeys.CTRL)
        dm.Key.KeyPress(ord('A'))
        dm.Key.KeyUp(VirtualKeys.CTRL)
        sleep(0.5)
        print('✓ 全选完成')

        # 移动到文档开头 (Ctrl+Home)
        print('\n→ 移动到文档开头 (Ctrl+Home)...')
        sleep(0.3)
        dm.Key.KeyDown(VirtualKeys.CTRL)
        dm.Key.KeyPress(36)  # VK_HOME = 36
        dm.Key.KeyUp(VirtualKeys.CTRL)
        sleep(0.3)
        print('✓ 光标已移动到开头')

        # 获取鼠标位置
        print('\n→ 获取鼠标当前位置...')
        x, y = dm.Mouse.position
        print(f'✓ 鼠标位置: ({x}, {y})')

    except Exception as e:
        print(f'✗ 演示操作失败: {e}')
        return False

    # 解绑窗口
    print('\n' + '=' * 60)
    print('步骤 5: 解绑窗口')
    print('=' * 60)

    try:
        dm.解绑窗口()
        print('✓ 窗口已解绑')
    except Exception as e:
        print(f'✗ 解绑窗口失败: {e}')

    # 测试总结
    print('\n' + '=' * 60)
    print('测试完成总结')
    print('=' * 60)
    print('✓ 所有测试步骤执行成功！')
    print('\n提示:')
    print('  - 记事本窗口保持打开状态')
    print('  - 可以查看输入的示例文本')
    print('  - 手动关闭记事本即可')
    print('\n' + '=' * 60)

    return True


def main():
    """主函数"""
    try:
        success = test_bind_and_input()
        if success:
            print('\n✓ 测试程序执行成功！')
            return 0
        else:
            print('\n✗ 测试程序执行失败！')
            return 1
    except KeyboardInterrupt:
        print('\n\n⚠ 用户中断测试')
        return 130
    except Exception as e:
        print(f'\n✗ 测试过程中发生异常: {e}')
        import traceback

        traceback.print_exc()
        return 1


if __name__ == '__main__':
    exit_code = main()
    sys.exit(exit_code)
