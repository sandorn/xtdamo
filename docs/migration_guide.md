# 迁移指南：从 bdtime 到内置时间工具

本文档说明如何从 `bdtime` 迁移到 xtdamo 内置的时间工具。

## 🔄 主要变更

### 1. 时间跟踪器

**之前 (bdtime):**

```python
from bdtime import tt

# 初始化
tt.__init__()

# 检查是否在指定时间内
while tt.during(10):  # 10秒超时
    # 执行操作
    pass

# 睡眠
tt.sleep(0.1)
```

**现在 (xtdamo):**

```python
from xtdamo.time_utils import TimeTracker
import time

# 创建时间跟踪器
time_tracker = TimeTracker(10)  # 10秒超时

# 检查是否在指定时间内
while time_tracker.during():
    # 执行操作
    pass

# 睡眠
time.sleep(0.1)
```

### 2. 虚拟键码

**之前 (bdtime):**

```python
from bdtime import vk

# 使用虚拟键码
key.press(vk.Constant)
key.down(vk.Constant)
```

**现在 (xtdamo):**

```python
from xtdamo.time_utils import VirtualKeys

# 使用虚拟键码
key.press(VirtualKeys.ENTER)
key.down(VirtualKeys.ENTER)
```

### 3. 时间格式化

**之前 (bdtime):**

```python
from bdtime import tt

# 获取当前时间
current_time = tt.now(1)  # 包含毫秒
```

**现在 (xtdamo):**

```python
from datetime import datetime

# 获取当前时间
current_time = datetime.now().strftime("%H:%M:%S.%f")[:-3]
```

## 📋 迁移检查清单

### ✅ 已完成的迁移

-   [x] `apiproxy.py` - 替换 `tt.during()` 为 `TimeTracker`
-   [x] `key.py` - 替换 `vk.Constant` 为 `VirtualKeys.ENTER`
-   [x] `鼠标相对位移.py` - 替换时间跟踪和睡眠函数
-   [x] `像素颜色捕捉.py` - 替换时间跟踪和格式化函数
-   [x] 移除所有 `bdtime` 导入
-   [x] 更新依赖管理

### 🔧 需要手动检查的地方

如果您有自定义代码使用了 `bdtime`，请检查以下内容：

1. **时间跟踪器使用**

    ```python
    # 检查是否有这样的代码
    from bdtime import tt
    while tt.during(timeout):
        # 需要替换为 TimeTracker
    ```

2. **虚拟键码使用**

    ```python
    # 检查是否有这样的代码
    from bdtime import vk
    key.press(vk.Constant)  # 需要替换为 VirtualKeys.ENTER
    ```

3. **时间格式化使用**
    ```python
    # 检查是否有这样的代码
    from bdtime import tt
    current_time = tt.now(1)  # 需要替换为 datetime
    ```

## 🚀 新功能优势

### 1. **更好的性能**

-   使用 `importlib.util.find_spec()` 检查依赖
-   避免不必要的模块导入
-   更快的启动时间

### 2. **更清晰的 API**

-   明确的时间跟踪器类
-   标准的虚拟键码常量
-   更好的类型注解

### 3. **更好的兼容性**

-   不依赖第三方包
-   使用标准库实现
-   更好的跨平台支持

## 🔍 故障排除

### 常见问题

1. **ImportError: No module named 'bdtime'**

    - 原因：代码中还有 `bdtime` 导入
    - 解决：按照迁移指南替换为新的导入

2. **AttributeError: 'TimeTracker' object has no attribute 'during'**

    - 原因：使用了错误的 API
    - 解决：使用 `time_tracker.during()` 而不是 `time_tracker.during(timeout)`

3. **NameError: name 'vk' is not defined**
    - 原因：没有导入 `VirtualKeys`
    - 解决：添加 `from xtdamo.time_utils import VirtualKeys`

### 调试技巧

```python
# 启用调试模式
import os
os.environ["XTDAMO_DEBUG"] = "1"

# 检查依赖状态
from xtdamo import DependencyChecker
DependencyChecker.print_dependency_report()
```

## 📚 相关文档

-   [配置管理指南](configuration.md)
-   [API 参考](api_reference.md)
-   [时间工具使用示例](../examples/dependency_check.py)
