#!/usr/bin/env python3
"""
xtdamo 发布脚本

用于自动化版本发布流程，包括：
1. 版本号更新
2. 分发包构建
3. 质量检查
4. PyPI发布
5. Git标签创建
"""

from __future__ import annotations

import argparse
import os
import subprocess
import sys
from pathlib import Path


def run_command(cmd, check=True):
    """运行命令并返回结果"""
    print(f'执行命令: {cmd}')
    result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
    if check and result.returncode != 0:
        print(f'命令执行失败: {cmd}')
        print(f'错误输出: {result.stderr}')
        sys.exit(1)
    return result


def update_version(version):
    """更新版本号"""
    print(f'更新版本号到: {version}')

    # 更新 pyproject.toml
    pyproject_path = Path('pyproject.toml')
    content = pyproject_path.read_text(encoding='utf-8')
    content = content.replace('version = "0.1.0"', f'version = "{version}"')
    pyproject_path.write_text(content, encoding='utf-8')

    # 更新 __init__.py
    init_path = Path('xtdamo/__init__.py')
    content = init_path.read_text(encoding='utf-8')
    content = content.replace('__version__ = "0.1.0"', f'__version__ = "{version}"')
    init_path.write_text(content, encoding='utf-8')

    print(f'版本号已更新到: {version}')


def build_package():
    """构建分发包"""
    print('构建分发包...')

    # 清理旧的构建文件
    if Path('dist').exists():
        run_command('rmdir /s /q dist', check=False)
    if Path('build').exists():
        run_command('rmdir /s /q build', check=False)
    if Path('xtdamo.egg-info').exists():
        run_command('rmdir /s /q xtdamo.egg-info', check=False)

    # 构建分发包
    result = run_command('python -m build')
    print('分发包构建完成')
    return result


def check_package():
    """检查分发包质量"""
    print('检查分发包质量...')
    result = run_command('twine check dist/*')
    print('分发包质量检查通过')
    return result


def upload_to_pypi():
    """上传到PyPI"""
    print('上传到PyPI...')

    # 检查是否设置了PyPI token
    token = os.getenv('TWINE_PASSWORD')
    if not token:
        print('警告: 未设置 TWINE_PASSWORD 环境变量')
        print('请设置PyPI token: set TWINE_PASSWORD=your-token')
        return False

    result = run_command('twine upload dist/*')
    print('上传到PyPI完成')
    return result


def create_git_tag(version):
    """创建Git标签"""
    print(f'创建Git标签: v{version}')

    # 添加所有更改
    run_command('git add .')

    # 提交更改
    run_command(f'git commit -m "feat: 发布版本 v{version}"')

    # 创建标签
    run_command(f'git tag -a v{version} -m "Release version {version}"')

    print(f'Git标签 v{version} 创建完成')


def main():
    parser = argparse.ArgumentParser(description='xtdamo 发布脚本')
    parser.add_argument('version', help='版本号 (例如: 0.1.1)')
    parser.add_argument('--skip-build', action='store_true', help='跳过构建步骤')
    parser.add_argument('--skip-check', action='store_true', help='跳过质量检查')
    parser.add_argument('--skip-upload', action='store_true', help='跳过PyPI上传')
    parser.add_argument('--skip-tag', action='store_true', help='跳过Git标签创建')

    args = parser.parse_args()

    print(f'开始发布版本: {args.version}')
    print('=' * 50)

    try:
        # 1. 更新版本号
        update_version(args.version)

        # 2. 构建分发包
        if not args.skip_build:
            build_package()

        # 3. 质量检查
        if not args.skip_check:
            check_package()

        # 4. 上传到PyPI
        if not args.skip_upload:
            upload_to_pypi()

        # 5. 创建Git标签
        if not args.skip_tag:
            create_git_tag(args.version)

        print('=' * 50)
        print(f'版本 {args.version} 发布完成!')

    except Exception as e:
        print(f'发布失败: {e}')
        sys.exit(1)


if __name__ == '__main__':
    main()
