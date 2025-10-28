# Cursor Rules 说明

本目录包含 TSC-Print-Service 项目的 Cursor AI 规则文件。这些规则帮助 AI 更好地理解项目结构、代码规范和最佳实践。

## 规则文件列表

### 1. `project-structure.mdc` ⚙️

**总是应用** (`alwaysApply: true`)

项目结构和整体架构说明，包括：

- 项目概述和平台信息
- 核心文件说明
- 关键依赖和环境要求
- API 端点列表
- 打印坐标系统

### 2. `python-style.mdc` 🐍

**适用于**: `*.py` 文件

Python 代码风格指南，包括：

- Python 3.10+ 语法规范
- 文档字符串格式
- 日志记录规范
- FastAPI 特定规范
- 打印机代码规范

### 3. `printer-development.mdc` 🖨️

**按需引用** (通过描述触发)

TSC 打印机开发指南，包括：

- 打印机初始化流程
- 坐标和尺寸计算
- 中文打印方案
- 常见打印命令
- 调试和测试工具
- 常见问题排查

### 4. `deployment.mdc` 🚀

**按需引用** (通过描述触发)

部署和环境配置指南，包括：

- macOS 开发环境设置
- Windows 部署环境设置
- 配置管理
- 生产环境建议
- 跨平台开发注意事项

### 5. `api-design.mdc` 📡

**按需引用** (通过描述触发)

FastAPI 接口设计规范，包括：

- **⚠️ API 文档同步规范（强制要求）**
- API 响应格式标准
- HTTP 状态码使用
- Pydantic 模型定义
- 路由定义规范
- 参数验证
- API 文档优化

**重要提醒**：任何接口变动必须同步更新 `API.md` 文档！

### 6. `error-handling.mdc` ⚠️

**按需引用** (通过描述触发)

错误处理和日志记录指南，包括：

- 错误处理层次
- 常见错误场景
- 日志记录规范
- 资源清理
- 调试技巧
- 错误恢复策略

### 7. `api-documentation.mdc` 📝

**适用于**: `main.py` 文件

API 文档同步提醒规则，包括：

- **🚨 强制规范：修改接口必须更新 API.md**
- 文档更新检查清单
- 文档更新模板和示例
- 常见错误和最佳实践
- 文档验证方法

**重要**：编辑 `main.py` 时会自动提醒更新文档！

## 如何使用这些规则

### 自动应用

- `project-structure.mdc` 会在所有 AI 对话中自动加载

### 文件类型触发

- 编辑 `.py` 文件时，`python-style.mdc` 会自动应用
- 编辑 `main.py` 文件时，`api-documentation.mdc` 会自动应用（🚨 提醒更新 API.md）

### 手动引用

在与 AI 对话时，提到相关主题会自动触发对应规则：

- "如何设置开发环境？" → `deployment.mdc`
- "打印机命令怎么写？" → `printer-development.mdc`
- "如何添加新的 API？" → `api-design.mdc`
- "错误如何处理？" → `error-handling.mdc`

## 规则文件格式

所有规则文件使用 Markdown 格式（`.mdc` 扩展名），包含 YAML frontmatter：

```markdown
---
alwaysApply: true # 总是应用
---

# 或

---

## globs: \*.py # 应用于特定文件类型

# 或

---

## description: 描述内容 # 通过描述触发
```

## 更新规则

如果需要修改或添加规则：

1. 编辑对应的 `.mdc` 文件
2. 保存后规则会立即生效
3. 无需重启 Cursor

## 规则优先级

1. `alwaysApply: true` 的规则优先级最高
2. `globs` 匹配的规则在编辑对应文件时应用
3. `description` 的规则在提到相关内容时应用

## 最佳实践

- 规则应该简洁明确
- 使用代码示例说明规范
- 引用项目中的实际文件（使用 `[filename](mdc:filename)` 格式）
- 定期更新规则以反映项目变化
