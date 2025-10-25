# 窗口绑定测试说明

## 快速开始

### 1. 准备环境

1. **打开记事本（Notepad）**

    - 按 `Win + R`
    - 输入 `notepad` 并回车
    - 保持记事本窗口打开

2. **以管理员身份运行**（推荐）
    - 右键点击 PowerShell 或命令提示符
    - 选择"以管理员身份运行"
    - 后台模式需要管理员权限

### 2. 运行测试

```bash
# 参数验证测试（无需管理员权限，无需窗口）
uv run examples/test_bind_params.py

# 窗口绑定测试（需要打开记事本）
uv run examples/test_bind_window.py
```

## 测试内容

### test_bind_params.py - 参数验证测试

测试参数传递和验证功能：

-   ✅ None 参数不覆盖默认值
-   ✅ 有效参数正确设置
-   ✅ 无效参数抛出错误
-   ✅ 参数范围验证

**优点**: 不需要管理员权限，不需要窗口，快速验证参数逻辑

### test_bind_window.py - 窗口绑定测试

测试实际的窗口绑定功能：

| 测试项              | 描述                     | 需要管理员 |
| ------------------- | ------------------------ | ---------- |
| 环境检查            | 检查管理员权限和大漠插件 | ❌         |
| 前台模式绑定        | 使用 normal 模式绑定     | ❌         |
| 后台模式绑定        | 使用 gdi/dx 模式绑定     | ✅         |
| 自定义配置          | 测试自定义参数           | ✅         |
| CoreEngine 直接调用 | 测试底层方法             | ❌         |
| 架构验证            | 验证组件关系             | ❌         |

## 常见问题

### 1. 错误代码 0：失败 (未知错误)

**症状**：

```
AssertionError: 窗口绑定失败!
  错误代码: 0
  错误信息: 失败 (未知错误)
```

**可能原因和解决方案**：

#### 原因 1: 没有管理员权限（最常见）

**解决方案**：

```bash
# 方法1: 以管理员身份运行整个脚本
右键点击 PowerShell → 以管理员身份运行

# 方法2: 使用前台模式（不需要管理员）
# 测试脚本会自动先尝试前台模式
```

#### 原因 2: 窗口未打开或窗口句柄无效

**解决方案**：

-   确保记事本已打开
-   窗口不要最小化
-   重新打开记事本再试

#### 原因 3: 大漠插件版本或注册问题

**解决方案**：

```python
# 查看大漠插件信息
from xtdamo import DmExcute
dm = DmExcute()
print(f"版本: {dm.ver()}")
print(f"ID: {dm.GetID()}")
```

### 2. 找不到窗口 (hwnd == 0)

**症状**：

```
❌ 未找到记事本窗口
```

**解决方案**：

1. 打开记事本程序
2. 确保窗口标题包含 "记事本" 或 使用英文版 "Notepad"
3. 如果使用其他语言版本，修改测试脚本中的窗口类名

### 3. 参数验证错误

**症状**：

```
ValueError: 无效的 display 值: xxx
```

**解决方案**：
这是正常的参数验证，查看有效值列表：

| 参数    | 有效值                                                               |
| ------- | -------------------------------------------------------------------- |
| display | `'normal'`, `'gdi'`, `'gdi2'`, `'dx'`, `'dx2'`                       |
| mouse   | `'normal'`, `'windows'`, `'windows2'`, `'windows3'`, `'dx'`, `'dx2'` |
| keypad  | `'normal'`, `'windows'`, `'dx'`                                      |
| mode    | `0, 1, 2, 3, 4, 5, 6, 7, 101, 103`                                   |

## 绑定模式对比

### 前台模式 (mode=0)

```python
dm.绑定窗口(
    hwnd,
    display='normal',
    mouse='normal',
    keypad='normal',
    public='',
    mode=0
)
```

**优点**：

-   ✅ 不需要管理员权限
-   ✅ 兼容性好
-   ✅ 适合调试

**缺点**：

-   ❌ 窗口必须在前台可见
-   ❌ 速度较慢
-   ❌ 会干扰用户操作

### 后台模式 (mode=101)

```python
dm.绑定窗口(hwnd)  # 使用默认配置
```

**优点**：

-   ✅ 窗口可以在后台
-   ✅ 速度快
-   ✅ 不干扰用户

**缺点**：

-   ❌ 需要管理员权限
-   ❌ 兼容性取决于游戏/程序
-   ❌ 可能被反作弊检测

## 推荐的测试顺序

1. **先运行参数验证测试**（快速验证逻辑）

    ```bash
    uv run examples/test_bind_params.py
    ```

2. **打开记事本**

3. **运行窗口绑定测试**

    ```bash
    # 普通用户运行（只有前台模式会成功）
    uv run examples/test_bind_window.py

    # 管理员运行（所有模式都可能成功）
    # 右键 PowerShell → 以管理员身份运行
    uv run examples/test_bind_window.py
    ```

## 测试结果解读

### 完全成功示例

```
✓ 通过 - 环境检查
✓ 通过 - 前台模式绑定（无需管理员）
✓ 通过 - 默认配置绑定（后台模式）
✓ 通过 - 自定义配置绑定
✓ 通过 - CoreEngine直接调用
✓ 通过 - 架构层次验证

总计: 6/6 测试通过
🎉 所有测试通过！架构统一完成！
```

### 部分成功示例（无管理员权限）

```
✓ 通过 - 环境检查
✓ 通过 - 前台模式绑定（无需管理员）
❌ 失败 - 默认配置绑定（后台模式）  ← 需要管理员
❌ 失败 - 自定义配置绑定          ← 需要管理员
✓ 通过 - CoreEngine直接调用
✓ 通过 - 架构层次验证

总计: 4/6 测试通过
⚠️  部分测试未通过，请检查相关功能
💡 建议：以管理员身份运行以测试后台模式
```

## 进阶使用

### 自定义测试窗口

修改测试脚本中的窗口查找部分：

```python
# 原始（查找记事本）
hwnd = dm.FindWindow('Notepad', '')

# 自定义（查找其他窗口）
hwnd = dm.FindWindow('', '窗口标题')
# 或
hwnd = dm.FindWindow('窗口类名', '')
```

### 调试绑定失败

```python
from xtdamo import DmExcute

dm = DmExcute()
hwnd = dm.FindWindow('Notepad', '')

# 尝试不同的绑定模式
modes = [
    ('前台', {'display': 'normal', 'mouse': 'normal', 'keypad': 'normal', 'mode': 0}),
    ('GDI', {'display': 'gdi', 'mouse': 'windows3', 'keypad': 'windows', 'mode': 101}),
    ('DX', {'display': 'dx', 'mouse': 'dx', 'keypad': 'dx', 'mode': 101}),
]

for name, config in modes:
    try:
        if dm.绑定窗口(hwnd, **config):
            print(f'✓ {name} 模式绑定成功')
            dm.解绑窗口()
        else:
            print(f'❌ {name} 模式绑定失败')
    except Exception as e:
        print(f'❌ {name} 模式错误: {e}')
```

## 获取帮助

如果遇到问题：

1. **查看环境检查输出** - 确认大漠插件版本和权限
2. **查看错误代码** - 参考 Config.ERROR_CODES
3. **尝试前台模式** - 排除权限问题
4. **查看大漠插件文档** - 了解具体的绑定模式说明

## 相关文档

-   [架构更新说明](../docs/architecture_update.md)
-   [配置说明](../docs/configuration.md)
-   [大漠插件官方文档](https://www.dmsoft.com/)
