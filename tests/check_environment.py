# !/usr/bin/env python3
"""
环境检查脚本 - 验证32位Python环境和大漠插件兼容性
"""

from __future__ import annotations

import platform
import sys
from pathlib import Path


def check_python_architecture():
    """检查Python架构"""
    print('=== Python环境检查 ===')
    print(f'Python版本: {sys.version}')
    print(f'Python架构: {platform.architecture()[0]}')
    print(f'平台: {platform.platform()}')

    if platform.architecture()[0] != '32bit':
        print('[X] 错误: 大漠插件仅支持32位Python环境!')
        print('请使用32位Python重新创建虚拟环境:')
        print('python -m venv .venv --python=python3.12-32')
        return False
    else:
        print('[OK] Python架构检查通过 (32位)')
        return True


def check_dm_plugin():
    """检查大漠插件"""
    print('\n=== 大漠插件检查 ===')

    # 检查默认路径
    dm_paths = [
        Path('xtdamo/.dm/dm.dll'),
        Path('xtdamo/dm.dll'),
        Path('dm.dll'),
    ]

    found_dm = False
    for dm_path in dm_paths:
        if dm_path.exists():
            print(f'[OK] 找到大漠插件: {dm_path}')
            found_dm = True
            break

    if not found_dm:
        print('[X] 未找到大漠插件 (dm.dll)')
        print('请将dm.dll放置在以下位置之一:')
        for path in dm_paths:
            print(f'  - {path}')
        return False

    return True


def check_dependencies():
    """检查依赖项"""
    print('\n=== 依赖项检查 ===')

    required_packages = [
        'win32api',  # pywin32的实际导入名称
        'typing_extensions',
    ]

    optional_packages = [
        'cryptography',
    ]

    missing_required = []
    missing_optional = []

    for package in required_packages:
        try:
            __import__(package)
            print(f'[OK] {package}')
        except ImportError:
            print(f'[X] {package} (必需)')
            missing_required.append(package)

    for package in optional_packages:
        try:
            __import__(package)
            print(f'[OK] {package} (可选)')
        except ImportError:
            print(f'[!] {package} (可选)')
            missing_optional.append(package)

    if missing_required:
        print(f'\n[X] 缺少必需依赖: {", ".join(missing_required)}')
        print('请运行: pip install -r requirements.txt')
        return False

    if missing_optional:
        print(f'\n[!] 缺少可选依赖: {", ".join(missing_optional)}')
        print('可选依赖用于加密功能，如需要请安装: pip install cryptography')

    return True


def check_xtdamo_import():
    """检查xtdamo模块导入"""
    print('\n=== xtdamo模块检查 ===')

    try:
        import xtdamo

        print('[OK] xtdamo模块导入成功')

        # 检查主要类
        from xtdamo import Config, DmCredentials, DmExcute

        print('[OK] 主要类导入成功')

        # 检查依赖检查工具
        from xtdamo.dependencies import check_dependency, get_available_dependencies

        print('[OK] 依赖检查工具可用')

        return True
    except ImportError as e:
        print(f'[X] xtdamo模块导入失败: {e}')
        return False


def main():
    """主检查函数"""
    print('xtdamo 环境检查工具')
    print('=' * 50)

    checks = [
        check_python_architecture,
        check_dm_plugin,
        check_dependencies,
        check_xtdamo_import,
    ]

    all_passed = True
    for check in checks:
        if not check():
            all_passed = False

    print('\n' + '=' * 50)
    if all_passed:
        print('[SUCCESS] 所有检查通过! 环境配置正确。')
        print('可以开始使用xtdamo了!')
    else:
        print('[FAILED] 环境检查失败，请根据上述提示修复问题。')

    return all_passed


if __name__ == '__main__':
    success = main()
    sys.exit(0 if success else 1)
