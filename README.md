# xtdamo

[![Version](https://img.shields.io/badge/version-0.2.0-blue.svg)](https://github.com/sandorn/xtdamo)
[![Python](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![License](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)

xtdamo 是一个基于大漠插件(Dm) 的现代化封装库，用于自动化操作，包括窗口管理、鼠标控制、键盘模拟、图像识别、文本查找等功能。适用于游戏脚本、自动化测试、RPA 等场景。

## ✨ 特性亮点

### 🏗️ 现代化架构设计

-   **分层架构**: 清晰的 `DmExcute -> ApiProxy -> CoreEngine` 三层设计
-   **智能路由**: 自动选择最佳方法实现，无需关心底层细节
-   **模块化**: `Key`、`Mouse` 独立模块，职责明确
-   **向后兼容**: 支持旧版本代码无缝迁移

### 🛡️ 健壮的错误处理

-   **参数验证**: 完整的参数范围检查和类型验证
-   **友好错误**: 详细的错误信息和诊断建议
-   **异常安全**: 完善的异常处理机制

### 📚 完整的文档支持

-   **Google Style**: 所有方法都有详细的文档字符串
-   **类型注解**: 完整的类型提示，IDE 智能提示友好
-   **示例丰富**: 每个功能都有实用的代码示例

### 🚀 增强功能

-   **安全点击**: `safe_click` 带随机延迟，防检测
-   **便利属性**: `position` 属性快速获取/设置鼠标位置
-   **高级操作**: 支持持续时间的点击、拖拽等复杂操作

## 简介

xtdamo 提供了对大漠插件的高级封装，简化了与窗口、鼠标、键盘和图像识别相关的操作。主要功能包括：

-   **窗口管理**: 窗口查找、绑定、属性获取
-   **鼠标操作**: 移动、点击、拖拽、滚轮
-   **键盘模拟**: 按键、组合键、文本输入
-   **图像识别**: 图像查找、颜色识别
-   **文本识别**: 文字查找、OCR
-   **高级功能**: 文件操作、注册表操作

## 安装

### 系统要求

-   **Python 3.8+ (32 位版本)** - 大漠插件仅支持 32 位 Python 环境
-   Windows 操作系统
-   大漠插件（dm.dll）

> **重要提示**: 大漠插件只能在 32 位 Python 环境下运行，请确保使用 32 位 Python 版本。

### 安装方法

1. **创建 32 位 Python 虚拟环境**：

```bash
# 确保使用32位Python创建虚拟环境
python -m venv .venv --python=python3.12-32  # 或指定32位Python路径
.venv\Scripts\activate  # Windows
```

2. **从源码安装**：

```bash
git clone https://github.com/sandorn/xtdamo.git
cd xtdamo
pip install -e .
```

3. **从 PyPI 安装**（计划中）：

```bash
pip install xtdamo
```

> **注意**: 请确保在 32 位 Python 环境中安装和运行项目。

### 大漠插件配置

将大漠插件（dm.dll）放置在项目目录中，或通过环境变量指定路径：

```bash
# 设置大漠插件认证信息（可选）
set DM_REG_CODE=your_registration_code
set DM_VER_INFO=your_version_info
```

## 架构设计

xtdamo 采用清晰的分层架构设计，确保代码的可维护性和可扩展性：

```
┌─────────────────────────────────────┐
│         DmExcute (主入口)           │
│  - 统一的调用接口                    │
│  - 自动方法路由                      │
└──────────────┬──────────────────────┘
               │
               ├──────────────────────┐
               │                      │
       ┌───────▼────────┐    ┌───────▼────────┐
       │   ApiProxy     │    │  CoreEngine    │
       │  (高级接口层)   │───>│  (核心引擎层)   │
       │                │    │                │
       │ - 中文友好API   │    │ - 底层核心方法  │
       │ - 智能错误处理  │    │ - 直接封装DM   │
       │ - 自动日志记录  │    │ - 基础功能实现  │
       └────────────────┘    └────────────────┘
```

### 核心特性

-   **分层架构**: 清晰的层次划分，职责明确
-   **智能路由**: 自动选择最合适的实现方法
-   **向后兼容**: 保持对旧代码的兼容性
-   **易于扩展**: 模块化设计，方便功能扩展

更多架构细节请参考 [架构更新说明](docs/architecture_update.md)。

## 📖 使用示例

### 快速开始

```python
from xtdamo import DmExcute

# 初始化（自动注册大漠插件）
dm = DmExcute()

# 查看版本信息
print(f"版本: {dm.ver()}")
print(f"库版本: {dm.__version__}")  # 输出: 0.2.0
```

### 窗口操作

```python
# 查找窗口
hwnd = dm.FindWindow("", "记事本")
if hwnd == 0:
    print("未找到窗口")
    exit(1)

# 绑定窗口（高级接口，带参数验证）
try:
    dm.绑定窗口(
        hwnd,
        display='gdi',      # 显示模式
        mouse='windows3',   # 鼠标模式
        keypad='windows',   # 键盘模式
        mode=101            # 绑定模式
    )
    print("绑定成功！")
except ValueError as e:
    print(f"参数错误: {e}")
except AssertionError as e:
    print(f"绑定失败: {e}")

# 使用默认配置绑定（推荐）
dm.绑定窗口(hwnd)  # 使用默认参数
```

### 鼠标操作（多种方式）

```python
# 方式1: 通过 DmExcute 主入口（自动路由）
dm.MoveTo(100, 200)        # 移动鼠标
dm.LeftClick()             # 左键点击

# 方式2: 使用便利属性
x, y = dm.Mouse.position   # 获取当前位置
dm.Mouse.position = (500, 300)  # 设置位置

# 方式3: 使用增强方法
dm.Mouse.safe_click(300, 400, auto_reset_pos=True)  # 安全点击
dm.Mouse.click_left(100, 200, t=1.0)  # 长按1秒

# 方式4: 拖拽操作
dm.Mouse.MoveTo(100, 100)
dm.Mouse.LeftDown()
dm.Mouse.MoveTo(200, 200)
dm.Mouse.LeftUp()
```

### 键盘操作

```python
# 通过 DmExcute 主入口
dm.KeyPressStr('Hello World')  # 输入文本
dm.KeyPress(13)                # 按回车键（VK_RETURN）

# 使用 VirtualKeys 常量
from xtdamo.time_utils import VirtualKeys
dm.Key.KeyPress(VirtualKeys.ENTER)
dm.Key.KeyPress(VirtualKeys.ESC)

# 组合键操作
dm.Key.KeyDown(VirtualKeys.CTRL)   # 按下Ctrl
dm.Key.KeyPress(ord('C'))          # 按C键
dm.Key.KeyUp(VirtualKeys.CTRL)     # 释放Ctrl

# 等待按键
if dm.Key.WaitKey(VirtualKeys.ESC, 5000):
    print("用户按下了ESC键")
```

### 图像识别与操作

```python
# 高级接口 - 找图并点击
success = dm.找图单击(0, 0, 1920, 1080, 'button.bmp', '000000', 0.9)
if success:
    print("找到并点击成功")

# 找图直到消失
dm.找图单击至消失(0, 0, 800, 600, 'close.bmp', max_retries=10)

# 获取坐标
found, x, y = dm.找图返回坐标(0, 0, 1920, 1080, 'target.bmp')
if found:
    print(f"图像位置: ({x}, {y})")
    dm.Mouse.safe_click(x, y)
```

### 文字识别与操作

```python
# 找字并点击
success = dm.找字单击(0, 0, 800, 600, '开始游戏', 'FFFFFF', 0.9)

# 简易识字
text = dm.简易识字(100, 100, 300, 200, 'FFFFFF', 0.9)
print(f"识别到的文字: {text}")

# 找字返回坐标
found, x, y = dm.找字返回坐标(0, 0, 800, 600, '确定', 'FFFFFF', 0.9)
if found:
    dm.Mouse.MoveTo(x, y)
    dm.Mouse.LeftClick()
```

### 智能查找（渐开螺旋）

```python
# 从中心点向外螺旋查找鼠标
found, x, y = dm.圆形渐开找鼠标(
    center_x=500,
    center_y=400,
    max_radius=200,
    pic_name='cursor.bmp'
)
if found:
    print(f"鼠标图片位置: ({x}, {y})")
```

### 完整示例 - 自动化脚本

```python
from xtdamo import DmExcute
from xtdamo.time_utils import sleep, VirtualKeys

def main():
    # 初始化
    dm = DmExcute()
    print(f"xtdamo 版本: {dm.__version__}")

    # 查找并绑定窗口
    hwnd = dm.FindWindow("", "目标程序")
    if hwnd == 0:
        print("未找到窗口")
        return

    # 绑定窗口（使用默认配置）
    dm.绑定窗口(hwnd)
    print("窗口绑定成功")

    # 执行自动化任务
    try:
        # 点击开始按钮
        if dm.找图单击(0, 0, 800, 600, 'start_button.bmp'):
            print("点击开始按钮成功")
            sleep(1)

        # 输入用户名
        dm.KeyPressStr('username')
        dm.KeyPress(VirtualKeys.TAB)

        # 输入密码
        dm.KeyPressStr('password')
        dm.KeyPress(VirtualKeys.ENTER)

        # 等待登录完成（找图确认）
        sleep(2)
        if dm.简易找图(0, 0, 800, 600, 'login_success.bmp'):
            print("登录成功！")

    finally:
        # 解绑窗口
        dm.解绑窗口()
        print("窗口已解绑")

if __name__ == '__main__':
    main()
```

## 贡献

欢迎贡献代码或提出建议！请参考 [贡献指南](CONTRIBUTING.md) 获取更多信息。

## 许可证

本项目遵循 [MIT 许可证](LICENSE)。
