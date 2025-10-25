# 架构更新说明 - 统一参数使用

## 更新时间

2025-10-25

## 更新目标

1. 统一参数使用，让 ApiProxy（高级接口）调用 CoreEngine（核心引擎）的方法，遵循分层架构设计原则
2. 添加参数验证机制，限制参数范围，提供友好的错误提示
3. 修复参数传递问题，确保 None 参数不覆盖默认值

## 架构层次

```
┌─────────────────────────────────────┐
│         DmExcute (主入口)           │
│  - 管理所有组件的生命周期            │
│  - 动态方法路由                      │
└──────────────┬──────────────────────┘
               │
               ├──────────────────────┐
               │                      │
       ┌───────▼────────┐    ┌───────▼────────┐
       │   ApiProxy     │    │  CoreEngine    │
       │  (高级接口层)   │───>│  (核心引擎层)   │
       │                │    │                │
       │ - 友好的中文API │    │ - 底层核心方法  │
       │ - 智能错误处理  │    │ - 直接封装DM   │
       │ - 自动日志记录  │    │ - 基础功能实现  │
       └────────────────┘    └───────┬────────┘
                                     │
                             ┌───────▼────────┐
                             │  dm_instance   │
                             │  (大漠插件)     │
                             └────────────────┘
```

## 主要变更

### 1. CoreEngine.BindWindow 增强

**文件**: `xtdamo/coreengine.py`

**变更内容**:

-   从简单的参数列表改为支持 Config 配置的灵活参数
-   添加 `public` 参数支持（用于后台最小化等高级功能）
-   使用 `BindWindowEx` 替代 `BindWindow`（功能更强大）
-   添加详细的文档注释和使用示例

**参数统一**:

```python
def BindWindow(
    self,
    hwnd: int,
    display: str | None = None,      # 默认 'gdi'
    mouse: str | None = None,        # 默认 'windows3'
    keypad: str | None = None,       # 默认 'windows'
    public: str = 'dx.public.fake.window.min|dx.public.hack.speed',
    mode: int | None = None,         # 默认 101
) -> int
```

### 2. ApiProxy 调用 CoreEngine

**文件**: `xtdamo/apiproxy.py`

**变更内容**:

-   构造函数添加 `core_engine` 参数
-   `绑定窗口` 方法优先调用 `core_engine.BindWindow`
-   `解绑窗口` 方法优先调用 `core_engine.UnBindWindow`
-   保留降级方案（当 core_engine 不可用时）

**调用层次**:

```python
ApiProxy.绑定窗口()
    ↓
CoreEngine.BindWindow()
    ↓
dm_instance.BindWindowEx()
```

### 3. DmExcute 初始化顺序调整

**文件**: `xtdamo/damo.py`

**变更内容**:

-   先创建 CoreEngine（底层）
-   再创建 ApiProxy 并传入 CoreEngine 实例
-   确保依赖关系正确

**初始化顺序**:

```python
1. CoreEngine(dm_instance)          # 核心引擎
2. Key(dm_instance)                 # 键盘模块
3. Mouse(dm_instance)               # 鼠标模块
4. ApiProxy(dm_instance, CoreEngine) # 高级接口（依赖核心引擎）
```

## 优势

### 1. 清晰的分层架构

-   **核心引擎层**: 直接封装大漠插件的底层功能
-   **高级接口层**: 提供友好的中文 API 和智能化处理
-   **主入口层**: 统一管理和动态路由

### 2. 代码复用

-   避免重复实现相同功能
-   ApiProxy 复用 CoreEngine 的核心逻辑
-   统一的配置管理（Config）

### 3. 易于维护

-   单一职责原则：每层专注自己的功能
-   修改底层逻辑只需更新 CoreEngine
-   高级接口自动继承底层改进

### 4. 向后兼容

-   保留降级方案，确保代码健壮性
-   即使 core_engine 不可用，仍可正常工作
-   不影响现有代码的使用

### 5. 更好的文档

-   每个方法都有详细的文档注释
-   包含参数说明、返回值、示例代码
-   注释清晰说明各层的职责

## 使用示例

### 底层使用（CoreEngine）

```python
from xtdamo import DmExcute

dm = DmExcute()

# 使用核心引擎的方法
hwnd = dm.CoreEngine.FindWindow("", "游戏窗口")
result = dm.CoreEngine.BindWindow(hwnd)
if result == 1:
    print("绑定成功")
```

### 高级接口使用（ApiProxy）

```python
from xtdamo import DmExcute

dm = DmExcute()

# 使用高级接口（推荐）
hwnd = dm.FindWindow("", "游戏窗口")
if dm.绑定窗口(hwnd):
    print("绑定成功")
    # 执行操作...
    dm.解绑窗口()
```

### 自动路由使用（最简单）

```python
from xtdamo import DmExcute

dm = DmExcute()

# DmExcute 自动路由到合适的组件
hwnd = dm.FindWindow("", "游戏窗口")  # 自动路由到 CoreEngine
if dm.绑定窗口(hwnd):                  # 自动路由到 ApiProxy
    print("绑定成功")
```

## 参数验证机制（新增）

### 1. 问题描述

之前的实现存在问题：

-   当传入 `display=None` 时，会覆盖默认配置为 `None`
-   没有参数验证，可能传入无效的模式值
-   错误提示不够友好

### 2. 解决方案

**Config.get_bind_config 方法改进**：

```python
@classmethod
def get_bind_config(cls, **kwargs) -> dict[str, Any]:
    """
    只有非 None 的参数才会覆盖默认配置，并且会验证参数的有效性
    """
    config = cls.DEFAULT_BIND_CONFIG.copy()

    # 只更新非 None 的参数，并验证其有效性
    for key, value in kwargs.items():
        if value is not None:
            # 验证参数名是否有效
            if key not in cls.BIND_MODES:
                raise ValueError(f'无效的配置参数: {key}')

            # 验证参数值是否在有效范围内
            if not cls.validate_bind_mode(key, value):
                raise ValueError(f'无效的 {key} 值: {value}')

            config[key] = value

    return config
```

### 3. 参数行为示例

```python
# 示例1: 不传参数 - 使用所有默认值
config = Config.get_bind_config()
# 结果: {'display': 'gdi', 'mouse': 'windows3', 'keypad': 'windows', 'mode': 101}

# 示例2: 传入 None - 不覆盖默认值
config = Config.get_bind_config(display=None, mouse='dx')
# 结果: {'display': 'gdi', 'mouse': 'dx', 'keypad': 'windows', 'mode': 101}

# 示例3: 传入有效值 - 覆盖默认值
config = Config.get_bind_config(display='dx2', mode=103)
# 结果: {'display': 'dx2', 'mouse': 'windows3', 'keypad': 'windows', 'mode': 103}

# 示例4: 传入无效值 - 抛出异常
try:
    config = Config.get_bind_config(display='invalid_mode')
except ValueError as e:
    print(e)  # 输出: 无效的 display 值: invalid_mode. 有效值: ['normal', 'gdi', 'gdi2', 'dx', 'dx2']
```

### 4. ApiProxy 错误处理改进

```python
def 绑定窗口(self, hwnd: int, display: str | None = None, ...):
    # 验证窗口句柄
    assert hwnd != 0, f'无效的窗口句柄: {hwnd}'

    try:
        # 调用 CoreEngine（参数验证在 Config 中进行）
        ret = self.core_engine.BindWindow(...)
    except ValueError as e:
        # 参数验证失败，重新抛出更友好的错误
        raise ValueError(f'绑定参数无效: {e}') from e

    # 检查绑定结果
    if ret != 1:
        error_msg = Config.get_error_message(ret)
        raise AssertionError(
            f'窗口绑定失败!\n'
            f'  窗口句柄: {hwnd}\n'
            f'  错误代码: {ret}\n'
            f'  错误信息: {error_msg}\n'
            f'  绑定配置: display={display or "gdi"}, ...'
        )

    return True
```

## 配置说明

所有绑定相关的配置都在 `Config` 类中统一管理：

```python
# 默认绑定配置
DEFAULT_BIND_CONFIG = {
    'display': 'gdi',       # GDI 模式，兼容性好
    'mouse': 'windows3',    # Windows 兼容模式
    'keypad': 'windows',    # Windows 消息模式
    'mode': 101,            # 后台模式
}

# 支持的绑定模式（用于参数验证）
BIND_MODES = {
    'display': ['normal', 'gdi', 'gdi2', 'dx', 'dx2'],
    'mouse': ['normal', 'windows', 'windows2', 'windows3', 'dx', 'dx2'],
    'keypad': ['normal', 'windows', 'dx'],
    'mode': [0, 1, 2, 3, 4, 5, 6, 7, 101, 103],
}
```

## 测试建议

1. **基本功能测试**

    - 测试使用默认配置绑定窗口
    - 测试自定义配置绑定窗口
    - 测试解绑窗口

2. **参数传递测试（新增）**

    - 测试不传参数使用默认值
    - 测试传入 None 不覆盖默认值
    - 测试传入有效值正确覆盖
    - 测试混合使用（部分 None，部分有效值）

3. **参数验证测试（新增）**

    - 测试有效参数能通过验证
    - 测试无效的 display 值抛出 ValueError
    - 测试无效的 mouse 值抛出 ValueError
    - 测试无效的 keypad 值抛出 ValueError
    - 测试无效的 mode 值抛出 ValueError
    - 测试无效的参数名抛出 ValueError

4. **分层测试**

    - 直接测试 CoreEngine.BindWindow
    - 测试 ApiProxy.绑定窗口（会调用 CoreEngine）
    - 测试 DmExcute 的自动路由

5. **降级测试**

    - 测试当 core_engine 为 None 时的降级行为
    - 确保降级方案正常工作

6. **错误处理测试**

    - 测试无效窗口句柄的处理
    - 测试绑定失败时的错误提示
    - 测试参数验证错误的友好提示

**运行测试脚本**：

```bash
# 参数传递和验证测试
python examples/test_bind_params.py

# 窗口绑定功能测试（需要打开记事本）
python examples/test_bind_window.py
```

## 后续优化建议

1. **更多方法迁移**

    - 将 ApiProxy 中其他直接调用 dm_instance 的方法改为调用 CoreEngine
    - 保持分层架构的一致性

2. **增加类型提示**

    - 为 core_engine 参数添加具体的类型提示（避免 Any）
    - 使用 TYPE_CHECKING 避免循环导入

3. **性能监控**

    - 添加方法调用链的性能监控
    - 记录每层的耗时

4. **单元测试**
    - 为每个层次编写单元测试
    - 测试分层调用的正确性

## 总结

本次更新实现了清晰的分层架构和完善的参数验证机制，让代码结构更加合理：

### 架构改进

✅ ApiProxy 作为高级接口层，调用 CoreEngine 的核心方法
✅ 统一了参数风格和配置管理
✅ 添加了详细的文档注释
✅ 保持了向后兼容性
✅ 提高了代码的可维护性和可扩展性

### 参数验证改进（新增）

✅ 修复了 None 参数覆盖默认值的问题
✅ 添加了参数范围验证，限制在有效值内
✅ 提供友好的错误提示，准确定位问题
✅ 参数验证集中在 Config 类，易于维护
✅ 支持混合使用默认值和自定义值

### 核心价值

-   **安全性提升**：参数验证防止无效配置
-   **易用性提升**：None 参数使用默认值，符合直觉
-   **可维护性提升**：配置和验证逻辑集中管理
-   **开发效率提升**：详细的错误提示加速问题定位

这种架构设计遵循了软件工程的最佳实践，为后续的功能扩展和维护打下了良好的基础。
