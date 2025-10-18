# 配置管理指南

xtdamo 提供了灵活的配置管理系统，支持多种配置方式和安全存储选项。

## 📁 配置文件结构

```
xtdamo/
├── config.py          # 基础配置管理（默认值、错误处理、绑定模式）
├── secure_config.py   # 认证信息管理（注册码、版本信息）
└── ...
```

## 🔧 基础配置 (config.py)

### 用途

-   提供默认配置值
-   错误代码映射
-   窗口绑定模式配置
-   配置验证功能

### 使用示例

```python
from xtdamo import Config

# 获取错误信息
error_msg = Config.get_error_message(1)  # "成功"

# 获取绑定配置
bind_config = Config.get_bind_config(display="dx", mode=103)

# 验证绑定模式
is_valid = Config.validate_bind_mode("display", "dx")  # True
```

### 可用配置

| 配置项                 | 默认值 | 说明               |
| ---------------------- | ------ | ------------------ |
| DEFAULT_MOUSE_DELAY    | 0.05   | 鼠标操作延迟（秒） |
| DEFAULT_KEYBOARD_DELAY | 0.05   | 键盘操作延迟（秒） |
| DEFAULT_SIMILARITY     | 0.9    | 图像识别相似度     |
| DEFAULT_TIMEOUT        | 5.0    | 默认超时时间（秒） |

## 🔐 认证信息管理 (secure_config.py)

### 用途

-   统一管理大漠插件认证信息
-   支持多种存储方式
-   提供安全存储选项

### 存储优先级

1. **环境变量** (最高优先级)
2. **Windows 凭据管理器**
3. **加密配置文件**
4. **明文配置文件**
5. **默认值** (最低优先级)

### 使用示例

```python
from xtdamo import DmCredentials, dm_credentials

# 使用全局实例
reg_code, ver_info = dm_credentials.get_dm_credentials()

# 创建自定义实例
cred = DmCredentials(config_dir="/custom/path")

# 设置认证信息
cred.set_dm_credentials("your_reg_code", "your_ver_info", "encrypted")
```

### 支持的存储方式

| 方式        | 安全性   | 说明               |
| ----------- | -------- | ------------------ |
| `env`       | ⭐⭐⭐   | 环境变量           |
| `windows`   | ⭐⭐⭐⭐ | Windows 凭据管理器 |
| `encrypted` | ⭐⭐⭐⭐ | 加密文件存储       |
| `plain`     | ⭐⭐     | 明文文件存储       |

## 🚀 快速开始

### 1. 使用默认配置

```python
from xtdamo import DmExcute

# 自动使用默认认证信息
dm = DmExcute()
```

### 2. 通过环境变量配置

```bash
# Windows
set DM_REG_CODE=your_registration_code
set DM_VER_INFO=your_version_info

# Linux/Mac
export DM_REG_CODE=your_registration_code
export DM_VER_INFO=your_version_info
```

```python
from xtdamo import DmExcute

# 自动读取环境变量
dm = DmExcute()
```

### 3. 通过代码配置

```python
from xtdamo import dm_credentials, DmExcute

# 设置认证信息
dm_credentials.set_dm_credentials(
    "your_reg_code",
    "your_ver_info",
    "encrypted"  # 加密存储
)

# 使用配置
dm = DmExcute()
```

## 🔒 安全建议

### 开发环境

-   使用环境变量或明文配置文件
-   避免在代码中硬编码敏感信息

### 生产环境

-   使用加密存储或密钥管理服务
-   定期轮换认证信息
-   限制配置文件访问权限

### 企业环境

-   使用 Windows 凭据管理器
-   集成企业密钥管理服务
-   实施访问控制和审计

## 📝 配置文件位置

### Windows

```
C:\Users\{username}\.xtdamo\
├── dm_credentials.json    # 明文配置
├── dm_credentials.enc     # 加密配置
└── dm_key.key            # 加密密钥
```

### Linux/Mac

```
~/.xtdamo/
├── dm_credentials.json    # 明文配置
├── dm_credentials.enc     # 加密配置
└── dm_key.key            # 加密密钥
```

## 🛠️ 高级配置

### 自定义配置目录

```python
from xtdamo import DmCredentials

# 使用自定义目录
cred = DmCredentials(config_dir="/secure/config/path")
```

### 批量配置管理

```python
from xtdamo import DmCredentials

cred = DmCredentials()

# 批量设置多个配置
configs = {
    "dm_reg_code": "reg_code_1",
    "dm_ver_info": "ver_info_1",
    "custom_setting": "value"
}

# 存储到配置文件
cred.store_plain_config(configs)
```

## 🔍 故障排除

### 常见问题

1. **认证失败**

    - 检查注册码和版本信息是否正确
    - 确认网络连接正常
    - 验证管理员权限

2. **配置文件读取失败**

    - 检查文件权限
    - 确认配置文件格式正确
    - 验证加密密钥完整性

3. **环境变量不生效**
    - 确认环境变量名称正确
    - 重启应用程序
    - 检查环境变量作用域

### 调试模式

```python
import os
os.environ["XTDAMO_DEBUG"] = "1"

from xtdamo import dm_credentials

# 启用详细日志
reg_code, ver_info = dm_credentials.get_dm_credentials()
print(f"Debug: 使用注册码 {reg_code}")
```

## 🔍 依赖检查

xtdamo 提供了强大的依赖检查工具，可以安全地检查可选依赖是否可用。

### 使用示例

```python
from xtdamo import (
    DependencyChecker,
    check_dependency,
    get_available_dependencies,
    CRYPTO_AVAILABLE,
    WIN32_AVAILABLE,
)

# 检查单个依赖
if check_dependency("cryptography"):
    print("加密功能可用")

# 使用预定义常量
if CRYPTO_AVAILABLE:
    from cryptography.fernet import Fernet

# 获取所有可用依赖
available = get_available_dependencies()
print(f"可用依赖: {available}")

# 打印完整依赖报告
DependencyChecker.print_dependency_report()
```

### 支持的依赖

| 依赖名称     | 包名         | 功能               | 是否必需 |
| ------------ | ------------ | ------------------ | -------- |
| cryptography | cryptography | 加密功能支持       | 可选     |
| win32cred    | pywin32      | Windows 凭据管理器 | 可选     |
| win32con     | pywin32      | Windows 常量支持   | 可选     |
| win32gui     | pywin32      | Windows GUI 支持   | 可选     |

### 安装缺失依赖

```python
from xtdamo import get_missing_dependencies, DependencyChecker

# 获取缺失依赖
missing = get_missing_dependencies()

# 获取安装命令
commands = DependencyChecker.get_installation_commands(missing)
for cmd in commands:
    print(f"运行: {cmd}")
```

## 📚 相关文档

-   [API 参考](api_reference.md)
-   [安全最佳实践](security.md)
-   [故障排除指南](troubleshooting.md)
