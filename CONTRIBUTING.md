# 🤝 贡献指南 (Contributing Guide)

感谢你考虑为 TSC-Print-Middleware 做出贡献！

本文档提供了如何为项目做出贡献的指导方针。

---

## 📋 目录

- [行为准则](#行为准则)
- [如何贡献](#如何贡献)
- [开发流程](#开发流程)
- [代码规范](#代码规范)
- [提交规范](#提交规范)
- [问题反馈](#问题反馈)
- [功能请求](#功能请求)

---

## 行为准则

### 我们的承诺

为了营造一个开放和友好的环境，我们承诺：

- 使用友好和包容的语言
- 尊重不同的观点和经验
- 优雅地接受建设性批评
- 关注对社区最有利的事情
- 对其他社区成员表示同理心

### 不可接受的行为

- 使用性化的语言或图像，以及不受欢迎的性关注或挑逗
- 捣乱/煽动性评论，人身或政治攻击
- 公开或私下骚扰
- 未经许可发布他人的私人信息
- 其他在专业环境中可被合理认为不适当的行为

---

## 如何贡献

### 🐛 报告 Bug

如果你发现了 Bug，请：

1. 检查 [Issues](https://github.com/你的用户名/TSC-Print-Middleware/issues) 确认问题尚未被报告
2. 创建新 Issue，使用 Bug Report 模板
3. 提供详细信息：
   - 复现步骤
   - 预期行为
   - 实际行为
   - 环境信息（操作系统、Python 版本、打印机型号）
   - 错误日志或截图

### ✨ 提出新功能

如果你有新功能的想法：

1. 检查 [Discussions](https://github.com/你的用户名/TSC-Print-Middleware/discussions) 看是否已有讨论
2. 创建新 Discussion 或 Issue，使用 Feature Request 模板
3. 描述：
   - 功能的使用场景
   - 预期的实现方式
   - 可能的替代方案

### 🔧 提交代码

1. Fork 本仓库
2. 创建功能分支 (`git checkout -b feature/AmazingFeature`)
3. 开发并测试你的更改
4. 提交更改 (`git commit -m 'Add some AmazingFeature'`)
5. 推送到分支 (`git push origin feature/AmazingFeature`)
6. 创建 Pull Request

---

## 开发流程

### 环境准备

1. **克隆仓库**

```bash
git clone https://github.com/你的用户名/TSC-Print-Middleware.git
cd TSC-Print-Middleware
```

2. **创建虚拟环境**

```bash
python -m venv venv
venv\Scripts\activate  # Windows
```

3. **安装依赖**

```bash
pip install -r requirements.txt
```

4. **运行测试**

```bash
# 启动服务
python main.py

# 在另一个终端测试
curl http://localhost:8000/health
```

### 开发新功能

1. **创建分支**

```bash
git checkout -b feature/your-feature-name
```

分支命名规范：

- `feature/` - 新功能
- `fix/` - Bug 修复
- `docs/` - 文档更新
- `refactor/` - 代码重构
- `test/` - 测试相关

2. **编写代码**

遵循 [代码规范](#代码规范)

3. **测试代码**

- 手动测试所有相关功能
- 确保不破坏现有功能
- 测试不同的输入情况

4. **更新文档**

如果你的更改影响了：

- API 接口 → 更新 `API.md`
- 使用方法 → 更新 `README.md`
- 配置选项 → 更新 `config.py` 注释

5. **提交更改**

参考 [提交规范](#提交规范)

---

## 代码规范

### Python 代码风格

遵循 [PEP 8](https://pep8.org/) 规范

**基本规则**：

```python
# 1. 使用 4 空格缩进
def my_function():
    pass

# 2. 函数和类之间空两行
class MyClass:
    pass


def another_function():
    pass

# 3. 导入顺序：标准库 → 第三方库 → 本地模块
import os
import sys

from fastapi import FastAPI

from printer import print_label

# 4. 使用类型提示
def print_text(text: str, qty: int = 1) -> bool:
    pass

# 5. 文档字符串
def my_function(param: str) -> int:
    """
    函数简短描述

    Args:
        param: 参数说明

    Returns:
        返回值说明
    """
    pass
```

### 命名规范

```python
# 变量和函数：snake_case
my_variable = 10
def my_function():
    pass

# 类名：PascalCase
class MyClass:
    pass

# 常量：UPPER_CASE
DEFAULT_WIDTH = "100"

# 私有变量/函数：前缀单下划线
def _internal_function():
    pass
```

### 注释规范

```python
# 单行注释：简洁明了
x = x + 1  # 增加计数器

# 多行注释：使用文档字符串
"""
这是一个多行注释
用于解释复杂逻辑
"""

# 中文注释：说明业务逻辑
# 计算打印区域的有效宽度（减去左右边距）
effective_width = width - 2 * margin
```

### API 设计规范

1. **一致的响应格式**

```python
# 成功
{
    "status": "ok",
    "message": "操作成功描述"
}

# 失败（使用 HTTPException）
{
    "detail": "错误描述"
}
```

2. **使用 Pydantic 模型**

```python
from pydantic import BaseModel, Field

class PrintJob(BaseModel):
    template: str = Field(..., description="模板名称")
    qty: int = Field(1, ge=1, le=100, description="打印数量")
```

3. **详细的文档字符串**

```python
@app.post("/print")
def api_print(job: PrintJob):
    """
    统一打印接口

    支持的模板：
    - single-text: 单行文本
    - double-text: 双行文本
    ...
    """
    pass
```

---

## 提交规范

### Commit Message 格式

使用 [Conventional Commits](https://www.conventionalcommits.org/zh-hans/) 规范：

```
<类型>(<范围>): <简短描述>

<详细描述>

<页脚>
```

**类型**：

- `feat`: 新功能
- `fix`: Bug 修复
- `docs`: 文档更新
- `style`: 代码格式（不影响功能）
- `refactor`: 重构
- `test`: 测试相关
- `chore`: 构建/工具相关

**示例**：

```bash
# 新功能
git commit -m "feat(template): 添加 image 元素支持"

# Bug 修复
git commit -m "fix(usb): 修复连接超时问题"

# 文档更新
git commit -m "docs(readme): 更新安装说明"

# 重构
git commit -m "refactor(printer): 优化坐标计算逻辑"
```

### Pull Request 规范

**标题**：简洁明了，描述主要变更

```
feat: 添加图片元素打印功能
fix: 修复 USB 连接稳定性问题
docs: 完善 API 文档示例
```

**描述**：

```markdown
## 变更说明

简要描述此 PR 的目的和主要变更

## 变更类型

- [ ] Bug 修复
- [x] 新功能
- [ ] 文档更新
- [ ] 代码重构

## 测试

说明如何测试这些变更：

1. 步骤 1
2. 步骤 2
3. 预期结果

## 截图（如适用）

添加截图帮助解释变更

## 检查清单

- [x] 代码遵循项目规范
- [x] 已更新相关文档
- [x] 已测试所有变更
- [x] 不破坏现有功能
```

---

## 问题反馈

### Bug Report 模板

```markdown
## Bug 描述

清晰简洁地描述 Bug

## 复现步骤

1. 执行操作 '...'
2. 点击 '...'
3. 查看 '...'
4. 出现错误

## 预期行为

描述你预期应该发生什么

## 实际行为

描述实际发生了什么

## 环境信息

- 操作系统: [例如 Windows 11]
- Python 版本: [例如 3.10.5]
- 项目版本: [例如 3.0.0]
- 打印机型号: [例如 TTE-344]

## 错误日志
```

粘贴相关的错误日志

```

## 截图

如果适用，添加截图帮助解释问题
```

---

## 功能请求

### Feature Request 模板

```markdown
## 功能描述

清晰简洁地描述你想要的功能

## 使用场景

描述这个功能的使用场景和价值

## 建议的实现方式

如果有想法，描述你认为应该如何实现

## 替代方案

描述你考虑过的其他解决方案

## 额外信息

添加其他相关信息或截图
```

---

## 开发技巧

### 调试技巧

1. **启用详细日志**

```python
import logging
logging.basicConfig(level=logging.DEBUG)
```

2. **使用交互式 API 文档**

访问 http://localhost:8000/docs 测试接口

3. **打印调试信息**

```python
logging.info(f"变量值: {variable}")
logging.debug(f"详细信息: {details}")
```

### 测试技巧

1. **快速测试接口**

```bash
# 健康检查
curl http://localhost:8000/health

# 测试打印
curl -X POST http://localhost:8000/print \
  -H "Content-Type: application/json" \
  -d '{"template": "single-text", "print_list": [{"text": "测试"}]}'
```

2. **使用 Python 测试脚本**

创建 `test_local.py`：

```python
import requests

def test_print():
    response = requests.post("http://localhost:8000/print", json={
        "template": "single-text",
        "print_list": [{"text": "测试"}]
    })
    print(response.json())

if __name__ == "__main__":
    test_print()
```

---

## 获取帮助

如果你有任何问题：

1. 📖 查看 [README.md](README.md) 和 [API.md](API.md)
2. 🔍 搜索 [Issues](https://github.com/你的用户名/TSC-Print-Middleware/issues)
3. 💬 在 [Discussions](https://github.com/你的用户名/TSC-Print-Middleware/discussions) 提问
4. 📧 联系维护者

---

## 致谢

感谢你的贡献！每一个 PR、Issue 和建议都让项目变得更好。

---

**记住**：好的代码不仅仅是能工作，还要易读、易维护、易扩展。

Happy Coding! 🚀
