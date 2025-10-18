# 环境设置指南

## 32 位 Python 环境要求

xtdamo 项目基于大漠插件，**仅支持 32 位 Python 环境**。这是因为大漠插件（dm.dll）只能在 32 位 Python 下运行。

## 环境设置步骤

### 1. 检查当前 Python 架构

```bash
python -c "import platform; print('Python架构:', platform.architecture()[0])"
```

如果显示 `64bit`，则需要安装 32 位 Python。

### 2. 安装 32 位 Python

#### 方法一：从官网下载

1. 访问 [Python 官网](https://www.python.org/downloads/)
2. 下载 32 位版本的 Python 3.8-3.12
3. 安装时选择"Add Python to PATH"

#### 方法二：使用包管理器

```bash
# 使用conda
conda create -n xtdamo python=3.12
conda activate xtdamo

# 使用pyenv (Windows)
pyenv install 3.12.0
pyenv global 3.12.0
```

### 3. 创建 32 位虚拟环境

```bash
# 确保使用32位Python
python -m venv .venv --python=python3.12-32

# 激活虚拟环境
# Windows
.venv\Scripts\activate
# Linux/Mac
source .venv/bin/activate
```

### 4. 验证环境

运行环境检查脚本：

```bash
python check_environment.py
```

### 5. 安装依赖

```bash
# 安装项目依赖
pip install -e .

# 或从requirements.txt安装
pip install -r requirements.txt
```

## 常见问题

### Q: 如何确认使用的是 32 位 Python？

A: 运行以下命令检查：

```python
import platform
print(platform.architecture())  # 应该显示 ('32bit', 'WindowsPE')
```

### Q: 64 位 Python 可以运行吗？

A: 不可以。大漠插件仅支持 32 位 Python 环境。

### Q: 虚拟环境创建失败？

A: 确保：

1. 使用 32 位 Python 创建虚拟环境
2. 路径中没有中文字符
3. 有足够的磁盘空间

### Q: 大漠插件找不到？

A: 将 `dm.dll` 放置在以下位置之一：

-   `xtdamo/.dm/dm.dll`
-   `xtdamo/dm.dll`
-   项目根目录的 `dm.dll`

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

## 性能优化

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
