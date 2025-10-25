# 测试程序改进日志

## 2025-10-25 - 修复重复注册问题

### 问题描述

测试程序出现大漠插件的注册、注销循环，原因是每个测试函数都创建新的 `DmExcute()` 实例。

### 原始代码问题

```python
def test_bind_with_frontend_mode():
    dm = DmExcute()  # ❌ 每个测试都创建新实例
    # ... 测试代码

def test_bind_with_default_config():
    dm = DmExcute()  # ❌ 再次创建，导致重复注册
    # ... 测试代码
```

**问题影响**：

-   每个测试都重新注册大漠插件
-   造成不必要的注册/注销循环
-   影响测试性能
-   可能触发插件限制

### 改进方案

#### 1. 修改 `check_environment()` 函数

**之前**：返回布尔值

```python
def check_environment():
    dm = DmExcute()
    # ... 检查代码
    return True  # 或 False
```

**现在**：返回 dm 实例

```python
def check_environment():
    try:
        dm = DmExcute()  # 只创建一次
        # ... 检查代码
        return dm  # ✅ 返回实例供后续使用
    except Exception as e:
        return None  # 失败返回 None
```

#### 2. 修改所有测试函数

**之前**：每个函数内部创建实例

```python
def test_bind_with_frontend_mode():
    dm = DmExcute()  # ❌ 重复创建
    hwnd = dm.FindWindow('Notepad', '')
    # ...
```

**现在**：接收 dm 参数

```python
def test_bind_with_frontend_mode(dm):
    """测试使用前台模式绑定窗口

    Args:
        dm: DmExcute 实例（避免重复创建）
    """
    hwnd = dm.FindWindow('Notepad', '')  # ✅ 使用传入的实例
    # ...
```

#### 3. 修改 main 函数

**之前**：

```python
def main():
    if not check_environment():  # 返回 True/False
        return

    results.append(('测试1', test_bind_with_frontend_mode()))  # 内部创建实例
    results.append(('测试2', test_bind_with_default_config()))  # 又创建实例
```

**现在**：

```python
def main():
    dm = check_environment()  # ✅ 获取实例
    if dm is None:
        return

    print('💡 提示：使用单一 dm 实例运行所有测试，避免重复注册/注销\n')
    results.append(('测试1', test_bind_with_frontend_mode(dm)))  # ✅ 传递实例
    results.append(('测试2', test_bind_with_default_config(dm)))  # ✅ 共享实例
```

### 改进效果

#### 之前（有问题）

```
[注册] 创建 DmExcute() - check_environment
[注销] 退出 check_environment

[注册] 创建 DmExcute() - test_bind_with_frontend_mode
[注销] 退出 test_bind_with_frontend_mode

[注册] 创建 DmExcute() - test_bind_with_default_config
[注销] 退出 test_bind_with_default_config

... 循环往复 ...
```

#### 现在（已修复）

```
[注册] 创建 DmExcute() - check_environment
  ↓
使用同一实例 - test_bind_with_frontend_mode
  ↓
使用同一实例 - test_bind_with_default_config
  ↓
使用同一实例 - test_bind_with_custom_config
  ↓
使用同一实例 - test_core_engine_direct
  ↓
使用同一实例 - test_architecture
  ↓
[注销] 程序结束时自动注销

只注册一次！✅
```

### 优点

1. **性能提升**

    - 只注册一次大漠插件
    - 减少不必要的初始化开销
    - 测试运行更快

2. **资源友好**

    - 避免频繁的注册/注销操作
    - 减少系统资源消耗
    - 不会触发插件使用限制

3. **代码清晰**

    - 明确表达"共享实例"的意图
    - 便于理解程序流程
    - 更容易维护

4. **稳定性提升**
    - 避免可能的注册冲突
    - 减少失败概率
    - 更可靠的测试结果

### 使用示例

```bash
# 运行改进后的测试
uv run examples/test_bind_window.py

# 预期输出
窗口绑定功能测试
============================================================
环境检查
✓ 管理员权限: 否
✓ 大漠插件: 已加载
  - 版本: 7.2129
  - ID: xxx

💡 提示：使用单一 dm 实例运行所有测试，避免重复注册/注销

============================================================
测试0: 使用前台模式绑定窗口（无需管理员）
============================================================
✓ 找到窗口句柄: 2428674
✓ 前台模式绑定成功
...
```

### 注意事项

1. **实例生命周期**

    - dm 实例在整个测试期间保持活跃
    - 程序结束时自动注销

2. **错误处理**

    - 如果环境检查失败（dm = None），所有测试都会被跳过
    - 这是预期行为，因为没有有效的 dm 实例

3. **向后兼容**
    - 不影响测试结果
    - 只是改进了实现方式
    - 所有测试功能保持不变

### 相关文件

-   `examples/test_bind_window.py` - 主测试文件（已修复）
-   `examples/test_bind_params.py` - 参数验证测试（无此问题）
-   `examples/README_测试说明.md` - 测试使用说明

### 技术细节

#### 函数签名变化

| 函数                            | 之前      | 现在               |
| ------------------------------- | --------- | ------------------ |
| check_environment()             | → bool    | → DmExcute \| None |
| test_bind_with_frontend_mode()  | () → bool | (dm) → bool        |
| test_bind_with_default_config() | () → bool | (dm) → bool        |
| test_bind_with_custom_config()  | () → bool | (dm) → bool        |
| test_core_engine_direct()       | () → bool | (dm) → bool        |
| test_architecture()             | () → bool | (dm) → bool        |

#### 实例管理

```python
# 创建实例（只在 check_environment 中）
dm = DmExcute()

# 传递实例（所有测试函数）
def test_xxx(dm):
    # 使用传入的 dm 实例
    hwnd = dm.FindWindow(...)
    dm.绑定窗口(hwnd)
    dm.解绑窗口()
```

### 总结

✅ **问题**：重复创建实例导致注册/注销循环
✅ **解决**：共享单一实例，只注册一次
✅ **效果**：性能提升，资源友好，更稳定
✅ **影响**：无破坏性变更，测试结果不变

这是一个重要的改进，解决了测试程序的核心问题，让测试更加高效和可靠！
