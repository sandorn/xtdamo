# 贡献指南

感谢您对 xtdamo 项目的关注！本文档将指导您如何为项目做出贡献。

## 开发环境设置

### 1. 克隆项目

```bash
git clone https://github.com/sandorn/xtdamo.git
cd xtdamo
```

### 2. 安装开发依赖

```bash
pip install -e ".[dev]"
```

### 3. 安装预提交钩子

```bash
pre-commit install
```

## 代码规范

### 1. 代码风格

-   使用 Black 进行代码格式化
-   使用 flake8 进行代码检查
-   使用 mypy 进行类型检查

### 2. 提交规范

使用约定式提交格式：

```
<type>[optional scope]: <description>

[optional body]

[optional footer(s)]
```

类型包括：

-   `feat`: 新功能
-   `fix`: 修复 bug
-   `docs`: 文档更新
-   `style`: 代码格式调整
-   `refactor`: 代码重构
-   `test`: 测试相关
-   `chore`: 构建过程或辅助工具的变动

### 3. 测试要求

-   新功能必须包含测试用例
-   测试覆盖率应保持在 80%以上
-   使用 pytest 作为测试框架

## 提交流程

1. Fork 项目到您的 GitHub 账户
2. 创建功能分支：`git checkout -b feature/your-feature-name`
3. 提交更改：`git commit -m "feat: add new feature"`
4. 推送分支：`git push origin feature/your-feature-name`
5. 创建 Pull Request

## 问题报告

在报告问题前，请确保：

1. 检查是否已有相同问题
2. 提供详细的复现步骤
3. 包含系统环境信息
4. 提供错误日志

## 功能请求

在提出功能请求前，请：

1. 检查是否已有类似功能
2. 详细描述功能需求
3. 说明使用场景
4. 考虑向后兼容性

## 许可证

通过贡献代码，您同意您的贡献将在 MIT 许可证下发布。
