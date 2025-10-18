# !/usr/bin/env python
"""
xtdamo 依赖检查示例
"""

from xtdamo import (
    DependencyChecker,
    check_dependency,
    get_available_dependencies,
    get_missing_dependencies,
    CRYPTO_AVAILABLE,
    WIN32_AVAILABLE,
    WIN32GUI_AVAILABLE,
)


def demo_basic_dependency_check():
    """演示基础依赖检查"""
    print("=== 基础依赖检查演示 ===")

    # 检查单个依赖
    crypto_available = check_dependency("cryptography")
    print(f"加密支持: {'[OK]' if crypto_available else '[X]'}")

    # 检查多个依赖
    deps = ["cryptography", "win32cred", "win32con"]
    results = DependencyChecker.check_dependencies(deps)

    for dep, available in results.items():
        status = "[OK]" if available else "[X]"
        print(f"{dep}: {status}")


def demo_advanced_dependency_check():
    """演示高级依赖检查"""
    print("\n=== 高级依赖检查演示 ===")

    # 获取所有可用依赖
    available = get_available_dependencies()
    print(f"可用依赖: {available}")

    # 获取缺失依赖
    missing = get_missing_dependencies()
    print(f"缺失依赖: {missing}")

    # 获取安装命令
    if missing:
        commands = DependencyChecker.get_installation_commands(missing)
        print("安装命令:")
        for cmd in commands:
            print(f"  {cmd}")


def demo_dependency_info():
    """演示依赖信息获取"""
    print("\n=== 依赖信息演示 ===")

    # 获取特定依赖信息
    crypto_info = DependencyChecker.get_dependency_info("cryptography")
    if crypto_info:
        print("加密依赖信息:")
        for key, value in crypto_info.items():
            print(f"  {key}: {value}")


def demo_predefined_checks():
    """演示预定义的依赖检查"""
    print("\n=== 预定义依赖检查演示 ===")

    print(f"加密支持: {'[OK]' if CRYPTO_AVAILABLE else '[X]'}")
    print(f"Windows凭据管理器: {'[OK]' if WIN32_AVAILABLE else '[X]'}")
    print(f"Windows GUI: {'[OK]' if WIN32GUI_AVAILABLE else '[X]'}")


def demo_full_report():
    """演示完整依赖报告"""
    print("\n=== 完整依赖报告 ===")
    DependencyChecker.print_dependency_report()


def demo_conditional_imports():
    """演示条件导入"""
    print("\n=== 条件导入演示 ===")

    if CRYPTO_AVAILABLE:
        try:
            from cryptography.fernet import Fernet

            print("[OK] 成功导入 cryptography.fernet.Fernet")
        except ImportError as e:
            print(f"[X] 导入失败: {e}")
    else:
        print("[X] cryptography 不可用，跳过导入")

    if WIN32_AVAILABLE:
        try:
            import win32cred
            import win32con

            print("[OK] 成功导入 win32cred 和 win32con")
        except ImportError as e:
            print(f"[X] 导入失败: {e}")
    else:
        print("[X] win32 模块不可用，跳过导入")


if __name__ == "__main__":
    demo_basic_dependency_check()
    demo_advanced_dependency_check()
    demo_dependency_info()
    demo_predefined_checks()
    demo_full_report()
    demo_conditional_imports()

    print("\n=== 依赖检查演示完成 ===")
