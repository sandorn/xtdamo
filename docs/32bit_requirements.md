# 32 位 Python 环境要求说明

## 重要提示

**xtdamo 项目基于大漠插件，仅支持 32 位 Python 环境。**

这是因为大漠插件（dm.dll）是 32 位 COM 组件，只能在 32 位 Python 环境下运行。

## 环境要求

### Python 版本

-   **Python 3.8+ (32 位版本)**
-   推荐使用 Python 3.12 (32 位)
-   不支持 64 位 Python

### 操作系统

-   Windows 操作系统
-   支持 Windows 7/8/10/11

### 大漠插件

-   dm.dll (32 位版本)
-   需要管理员权限注册

## 环境设置步骤

### 1. 检查当前 Python 架构

```bash
python -c "import platform; print('Python架构:', platform.architecture()[0])"
```

### 2. 安装 32 位 Python

如果当前是 64 位 Python，需要安装 32 位版本：

#### 方法一：官网下载

1. 访问 [Python 官网](https://www.python.org/downloads/)
2. 下载 32 位版本的 Python
3. 安装时选择"Add Python to PATH"

#### 方法二：使用包管理器

```bash
# 使用conda
conda create -n xtdamo python=3.12
conda activate xtdamo

# 使用pyenv
pyenv install 3.12.0
pyenv global 3.12.0
```

### 3. 创建 32 位虚拟环境

```bash
# 确保使用32位Python
python -m venv .venv --python=python3.12-32

# 激活虚拟环境
.venv\Scripts\activate  # Windows
```

### 4. 验证环境

运行环境检查脚本：

```bash
python check_environment.py
```

### 5. 安装依赖

```bash
pip install -e .
```

## 常见问题

### Q: 为什么需要 32 位 Python？

A: 大漠插件（dm.dll）是 32 位 COM 组件，只能在 32 位 Python 环境下运行。这是大漠插件的限制，不是 xtdamo 项目的限制。

### Q: 64 位 Python 可以运行吗？

A: 不可以。即使安装了 32 位大漠插件，64 位 Python 也无法调用 32 位 COM 组件。

### Q: 如何确认使用的是 32 位 Python？

A: 运行以下命令：

```python
import platform
print(platform.architecture())  # 应该显示 ('32bit', 'WindowsPE')
```

### Q: 虚拟环境创建失败？

A: 确保：

1. 使用 32 位 Python 创建虚拟环境
2. 路径中没有中文字符
3. 有足够的磁盘空间
4. 以管理员权限运行

### Q: 大漠插件注册失败？

A: 确保：

1. 以管理员权限运行
2. 使用 32 位 Python 环境
3. dm.dll 文件完整且未损坏
4. 系统支持 COM 组件

## 开发环境配置

### IDE 配置

#### VSCode

```json
{
    "python.defaultInterpreterPath": "./.venv/Scripts/python.exe",
    "python.terminal.activateEnvironment": true
}
```

#### PyCharm

1. File → Settings → Project → Python Interpreter
2. 选择 `.venv/Scripts/python.exe`

### 环境变量

```bash
# 设置大漠插件路径（可选）
set DM_DLL_PATH=D:\CODES\xtdamo\xtdamo\.dm\dm.dll

# 设置认证信息（可选）
set DM_REG_CODE=your_registration_code
set DM_VER_INFO=your_version_info
```

## 性能优化建议

### 1. 虚拟环境优化

```bash
# 使用pip-tools管理依赖
pip install pip-tools
pip-compile requirements.in
pip-sync requirements.txt
```

### 2. 缓存配置

```bash
# 设置pip缓存
pip config set global.cache-dir "D:/TMP/pip_cache"
```

### 3. 开发工具配置

```bash
# 安装开发依赖
pip install -e ".[dev]"

# 运行代码检查
python -m ruff check xtdamo/
python -m ruff format xtdamo/
```

## 故障排除

### 问题 1：COM 对象创建失败

-   确保以管理员权限运行
-   检查大漠插件是否正确注册
-   验证 32 位 Python 环境

### 问题 2：模块导入失败

-   检查虚拟环境是否激活
-   验证依赖是否正确安装
-   运行 `python check_environment.py`

### 问题 3：权限错误

-   以管理员身份运行命令提示符
-   检查 UAC 设置
-   确保有足够的系统权限

### 问题 4：架构不匹配

-   确认使用 32 位 Python
-   检查大漠插件版本
-   重新创建虚拟环境

## 总结

xtdamo 项目需要 32 位 Python 环境才能正常运行。这是大漠插件的技术限制，不是项目本身的问题。请按照上述步骤正确配置 32 位 Python 环境。
