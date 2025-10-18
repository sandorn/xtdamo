# 发布脚本说明

## 发布脚本 (release.py)

自动化版本发布流程的 Python 脚本。

### 功能特性

-   **版本号更新**: 自动更新 `pyproject.toml` 和 `__init__.py` 中的版本号
-   **分发包构建**: 使用 `python -m build` 构建标准分发包
-   **质量检查**: 使用 `twine check` 验证分发包质量
-   **PyPI 发布**: 自动上传到 PyPI 平台
-   **Git 标签**: 创建版本标签和提交

### 使用方法

#### 基本用法

```bash
# 发布新版本
python scripts/release.py 0.1.1

# 跳过某些步骤
python scripts/release.py 0.1.1 --skip-upload --skip-tag
```

#### 参数说明

-   `version`: 版本号 (必需)
-   `--skip-build`: 跳过构建步骤
-   `--skip-check`: 跳过质量检查
-   `--skip-upload`: 跳过 PyPI 上传
-   `--skip-tag`: 跳过 Git 标签创建

#### 环境变量

```bash
# 设置PyPI token
set TWINE_PASSWORD=your-pypi-token

# 或者使用环境变量文件
echo TWINE_PASSWORD=your-pypi-token > .env
```

### 发布流程

1. **版本号更新**

    - 更新 `pyproject.toml` 中的版本号
    - 更新 `xtdamo/__init__.py` 中的 `__version__`

2. **分发包构建**

    - 清理旧的构建文件
    - 使用 `python -m build` 构建分发包
    - 生成 `.tar.gz` 和 `.whl` 文件

3. **质量检查**

    - 使用 `twine check` 验证分发包
    - 检查元数据完整性
    - 验证分发包格式

4. **PyPI 发布**

    - 使用 `twine upload` 上传到 PyPI
    - 需要设置 `TWINE_PASSWORD` 环境变量

5. **Git 标签**
    - 添加所有更改到 Git
    - 创建提交记录
    - 创建版本标签

### 示例

#### 发布补丁版本

```bash
python scripts/release.py 0.1.1
```

#### 发布功能版本

```bash
python scripts/release.py 0.2.0
```

#### 仅构建和检查，不上传

```bash
python scripts/release.py 0.1.1 --skip-upload --skip-tag
```

#### 仅更新版本号

```bash
python scripts/release.py 0.1.1 --skip-build --skip-check --skip-upload --skip-tag
```

### 注意事项

1. **PyPI Token**: 需要有效的 PyPI token 才能上传
2. **Git 状态**: 确保工作目录干净，没有未提交的更改
3. **版本号**: 遵循语义化版本规范
4. **网络连接**: 上传到 PyPI 需要网络连接

### 故障排除

#### 构建失败

```bash
# 清理构建文件
rmdir /s /q dist build xtdamo.egg-info

# 重新构建
python -m build
```

#### 上传失败

```bash
# 检查token设置
echo %TWINE_PASSWORD%

# 手动上传
twine upload dist/*
```

#### Git 标签失败

```bash
# 检查Git状态
git status

# 手动创建标签
git tag -a v0.1.1 -m "Release version 0.1.1"
```

### 版本规范

遵循 [语义化版本规范](https://semver.org/lang/zh-CN/)：

-   **主版本号**: 不兼容的 API 修改
-   **次版本号**: 向下兼容的功能性新增
-   **修订号**: 向下兼容的问题修正

### 相关文档

-   [版本迭代规范](../docs/versioning.md)
-   [贡献指南](../CONTRIBUTING.md)
-   [PyPI 发布指南](https://packaging.python.org/tutorials/packaging-projects/)
