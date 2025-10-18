# xtdamo

xtdamo 是一个基于大漠插件（Dm) 的封装库，用于自动化操作，包括窗口管理、鼠标控制、键盘模拟、图像识别、文本查找等功能。适用于游戏脚本、自动化测试等场景。

## 简介

xtdamo 提供了对大漠插件的高级封装，简化了与窗口、鼠标、键盘和图像识别相关的操作。主要功能包括：

- 窗口绑定与管理
- 鼠标移动与点击
- 键盘按键模拟
- 图像识别与查找
- 文本识别与查找
- 文件与注册表操作

## 安装

确保你已经安装了 Python 3.x，并可以通过 pip 安装 xtdamo：

```bash
pip install xtdamo
```

此外，你需要将大漠插件（dm.dll）放置在项目目录中，或指定其路径。

## 使用示例

### 初始化大漠插件

```python
from xtdamo import DmExcute

dm = DmExcute(dm_dirpath="path_to_dm_dll")
```

### 绑定窗口

```python
from xtdamo.apiproxy import ApiProxy

api_proxy = ApiProxy(dm)
hwnd = 123456  # 窗口句柄
api_proxy.绑定窗口(hwnd)
```

### 查找并点击图像

```python
api_proxy.找图单击(0, 0, 800, 600, "image.png")
```

### 查找并点击文字

```python
api_proxy.找字单击(0, 0, 800, 600, "开始", "FFFFFF")
```

### 鼠标操作

```python
from xtdamo.mouse import Mouse

mouse = Mouse(dm)
mouse.move_to(100, 200)  # 移动鼠标到指定坐标
mouse.click_left(100, 200)  # 左键点击
```

### 键盘操作

```python
from xtdamo.key import Key

key = Key(dm)
key.press("A")  # 按下 A 键
key.down("Enter")  # 按下 Enter 键
key.up("Enter")  # 释放 Enter 键
```

## 贡献

欢迎贡献代码或提出建议！请参考 [贡献指南](CONTRIBUTING.md) 获取更多信息。

## 许可证

本项目遵循 [MIT 许可证](LICENSE)。