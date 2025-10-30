# 🖨️ TSC-Print-Middleware

> **零驱动 TSC 打印机 USB 中间件** - 模板化打印 | RESTful API | 开箱即用

[English](README_EN.md) | 简体中文

[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)
[![Python 3.10+](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/downloads/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.120-green.svg)](https://fastapi.tiangolo.com/)
[![PRs Welcome](https://img.shields.io/badge/PRs-welcome-brightgreen.svg)](CONTRIBUTING.md)

---

## ✨ 特性

- 🚀 **零驱动** - 无需安装打印机驱动，USB 直接通信
- 🎨 **模板系统** - 5 种预设模板 + 完全自定义布局
- 🌐 **RESTful API** - FastAPI 提供标准 HTTP 接口
- 🇨🇳 **完美中文支持** - Windows 宋体字库
- 📦 **开箱即用** - pip install 一键安装
- 🔧 **高度灵活** - 从简单到复杂，满足各种需求

---

## 📸 演示

### 预设模板效果

```
┌─────────────────────┐
│                     │
│    单行文本居中      │
│                     │
└─────────────────────┘

┌─────────────────────┐
│    第一行文本        │
├─────────────────────┤
│    第二行文本        │
└─────────────────────┘

┌─────────────────────┐
│    ████████████     │
│    ██ QR CODE ██    │
│    ████████████     │
│                     │
│      产品名称        │
└─────────────────────┘
```

---

## 🎯 应用场景

- ✅ 仓库物料标签打印
- ✅ 商品条码/二维码打印
- ✅ 快递单号打印
- ✅ 资产管理标签
- ✅ 库存盘点标签

---

## 🚀 快速开始

### 环境要求

- **操作系统**: Windows 10/11
- **Python**: 3.10 或更高版本
- **打印机**: TSC 系列打印机（USB 连接）
- **系统依赖**: VC2015-2022 x86 运行库

### 安装步骤

#### 1. 克隆项目

```bash
git clone https://github.com/你的用户名/TSC-Print-Middleware.git
cd TSC-Print-Middleware
```

#### 2. 创建虚拟环境

```cmd
python -m venv venv
venv\Scripts\activate
```

#### 3. 安装依赖

```cmd
pip install -r requirements.txt
```

#### 4. 启动服务

```cmd
python main.py
```

服务将在 `http://localhost:8000` 启动

访问 http://localhost:8000/docs 查看交互式 API 文档 📖

---

## 📚 模板系统

TSC-Print-Middleware 提供 **5 种打印模板**，从简单到复杂，满足各种需求。

### 1️⃣ single-text - 单行文本

单行文本水平垂直居中

```python
import requests

requests.post("http://localhost:8000/print", json={
    "template": "single-text",
    "print_list": [
        {"text": "物料编号: A12345"}
    ]
})
```

### 2️⃣ double-text - 双行文本

每张纸打印两行文本（上下布局）

```python
requests.post("http://localhost:8000/print", json={
    "template": "double-text",
    "print_list": [
        {"text1": "第一行文本"},
        {"text2": "第二行文本"}
    ]
})
```

### 3️⃣ qrcode-with-text - 二维码+文本

二维码在上，文本在下，中心对齐

```python
requests.post("http://localhost:8000/print", json={
    "template": "qrcode-with-text",
    "print_list": [
        {
            "qrcode": "https://example.com/product/12345",
            "text": "产品编号: 12345"
        }
    ]
})
```

### 4️⃣ barcode-with-text - 条形码+文本

条形码在上，文本在下，中心对齐

```python
requests.post("http://localhost:8000/print", json={
    "template": "barcode-with-text",
    "print_list": [
        {
            "barcode": "1234567890",
            "text": "订单号: 1234567890"
        }
    ]
})
```

### 5️⃣ custom - 完全自定义布局

高级用户可以完全控制每个元素的位置和样式

```python
requests.post("http://localhost:8000/print", json={
    "template": "custom",
    "layout": {
        "width": 100,
        "height": 80,
        "elements": [
            {
                "type": "text",
                "x": 100,
                "y": 100,
                "text": "自定义标题",
                "font_size": 56,
                "font_name": "宋体"
            },
            {
                "type": "qrcode",
                "x": 300,
                "y": 300,
                "content": "https://example.com",
                "size": 10
            },
            {
                "type": "barcode",
                "x": 100,
                "y": 600,
                "content": "123456789",
                "height": 80,
                "barcode_type": "128"
            }
        ]
    },
    "qty": 1
})
```

---

## 🔧 API 接口

### 基础接口

#### GET `/` - 服务信息

```bash
curl http://localhost:8000/
```

#### GET `/health` - 健康检查

```bash
curl http://localhost:8000/health
```

#### POST `/test` - 测试 USB 连接

```bash
curl -X POST http://localhost:8000/test
```

### 打印接口

#### POST `/print` - 统一打印接口

详细文档请查看 [API.md](API.md)

---

## 📖 配置说明

### 纸张配置

在 `config.py` 中修改默认纸张尺寸：

```python
DEFAULT_WIDTH = "100"   # 标签宽度(mm) - 10cm
DEFAULT_HEIGHT = "80"   # 标签高度(mm) - 8cm
```

### DPI 设置

根据你的打印机型号调整 DPI：

```python
# TTE-344/345 (300 DPI)
DPI_RATIO = 11.81  # dots per mm

# TTP-244/247 (203 DPI)
# DPI_RATIO = 8.0

# TTP-644 (600 DPI)
# DPI_RATIO = 23.62
```

### 模板参数

修改预设模板的字体大小、间距等参数：

```python
# single-text & double-text
TYPE1_FONT_HEIGHT = 56  # 字体高度
TYPE1_FONT_NAME = "宋体"

# qrcode-with-text & barcode-with-text
TYPE2_FONT_HEIGHT = 48
TYPE2_QR_SIZE = 12  # 二维码大小
```

---

## 🏗️ 架构设计

```
┌─────────────────┐      HTTP/JSON       ┌──────────────────────┐
│   前端应用       │ ─────────────────>  │  FastAPI Service     │
│  (任何语言)      │                      │   TSC-Print-MW       │
└─────────────────┘                      └──────────────────────┘
                                                   │
                                                   │ pythonnet
                                                   │ + tsclib
                                                   ▼
                                         ┌──────────────────────┐
                                         │   TSC Printer        │
                                         │   (USB Connection)   │
                                         └──────────────────────┘
```

**核心技术栈**:

- FastAPI - Web 框架
- pythonnet - Python 与 .NET 互操作
- tsclib - TSC 打印机控制库

---

## 🛠️ 高级用法

### 批量打印

所有模板都支持批量打印：

```python
# 批量打印10个二维码标签
requests.post("http://localhost:8000/print", json={
    "template": "qrcode-with-text",
    "print_list": [
        {"qrcode": f"https://example.com/{i}", "text": f"产品-{i}"}
        for i in range(1, 11)
    ]
})
```

### 坐标系统

- **原点**: 左上角 (0, 0)
- **单位**: dots（点）
- **转换公式**: `dots = mm × DPI_RATIO`
- **示例**: 100mm × 11.81 = 1181 dots (300 DPI)

### 自定义元素

#### 文本元素

```json
{
  "type": "text",
  "x": 100, // X坐标 (dots)
  "y": 100, // Y坐标 (dots)
  "text": "文本内容",
  "font_size": 48, // 字体大小 (12-120)
  "font_name": "宋体" // 字体名称
}
```

#### 二维码元素

```json
{
  "type": "qrcode",
  "x": 200, // X坐标
  "y": 200, // Y坐标
  "content": "二维码内容", // URL或文本
  "size": 10 // 单元宽度 (1-10)
}
```

#### 条形码元素

```json
{
  "type": "barcode",
  "x": 100, // X坐标
  "y": 400, // Y坐标
  "content": "123456789", // 条形码内容
  "height": 80, // 高度 (30-300)
  "barcode_type": "128" // 类型 (128, EAN13等)
}
```

---

## 📦 项目结构

```
TSC-Print-Middleware/
├── main.py              # FastAPI 应用入口
├── printer.py           # 打印机核心模块
├── config.py            # 配置文件
├── requirements.txt     # 依赖管理
├── test_print.py        # 测试脚本
├── README.md            # 项目说明
├── API.md               # API 文档
├── LICENSE              # MIT 许可证
├── CHANGELOG.md         # 变更日志
├── CONTRIBUTING.md      # 贡献指南
└── examples/            # 示例代码
    ├── python_client.py
    └── javascript_client.js
```

---

## 🤝 贡献

欢迎贡献！请查看 [CONTRIBUTING.md](CONTRIBUTING.md) 了解详情。

### 快速贡献步骤

1. Fork 本项目
2. 创建特性分支 (`git checkout -b feature/AmazingFeature`)
3. 提交更改 (`git commit -m 'Add some AmazingFeature'`)
4. 推送到分支 (`git push origin feature/AmazingFeature`)
5. 开启 Pull Request

---

## ❓ 常见问题

### 1. 找不到打印机

**问题**: 提示 "USB 打印机连接失败"

**解决**:

- 检查打印机是否通过 USB 连接到电脑
- 确认打印机电源已开启
- 检查 Windows 设备管理器中是否识别到打印机

### 2. 中文乱码

**问题**: 打印的中文显示为乱码或方块

**解决**:

- 确认 Windows 系统已安装宋体字库
- 检查 Python 环境编码为 UTF-8
- 在 config.py 中尝试其他中文字体（如"微软雅黑"）

### 3. 打印位置偏移

**问题**: 打印内容位置不准确

**解决**:

- 检查 DPI_RATIO 是否与你的打印机型号匹配
- 执行纸张校准：`python -c "from printer import calibrate_paper; calibrate_paper()"`
- 调整 config.py 中的 PRINT_MARGIN 参数

### 4. 依赖安装失败

**问题**: `pip install -r requirements.txt` 失败

**解决**:

- 确保已安装 VC2015-2022 x86 运行库
- 使用管理员权限运行命令提示符
- 尝试单独安装 pythonnet: `pip install pythonnet==3.0.5`

---

## 📝 许可证

本项目采用 MIT 许可证 - 查看 [LICENSE](LICENSE) 文件了解详情

---

## 🙏 致谢

- [FastAPI](https://fastapi.tiangolo.com/) - 现代化的 Web 框架
- [pythonnet](https://github.com/pythonnet/pythonnet) - Python 与 .NET 互操作
- [TSC](https://www.tscprinters.com/) - TSC 打印机

---

## 📮 联系方式

- 问题反馈: [GitHub Issues](https://github.com/你的用户名/TSC-Print-Middleware/issues)
- 功能建议: [GitHub Discussions](https://github.com/你的用户名/TSC-Print-Middleware/discussions)

---

**⭐ 如果这个项目对你有帮助，请给个 Star！**
