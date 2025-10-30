# 📖 TSC-Print-Middleware API 文档

## 目录

- [服务信息](#服务信息)
- [基础接口](#基础接口)
- [打印接口](#打印接口)
  - [模板 1: single-text](#1-single-text---单行文本)
  - [模板 2: double-text](#2-double-text---双行文本)
  - [模板 3: qrcode-with-text](#3-qrcode-with-text---二维码文本)
  - [模板 4: barcode-with-text](#4-barcode-with-text---条形码文本)
  - [模板 5: custom](#5-custom---完全自定义)
- [错误处理](#错误处理)
- [代码示例](#代码示例)

---

## 服务信息

- **服务名称**: TSC-Print-Middleware
- **版本**: 3.0.0
- **默认端口**: 8000
- **纸张规格**: 10cm × 8cm (100mm × 80mm)
- **连接方式**: USB
- **API 文档**: http://localhost:8000/docs (Swagger UI)

---

## 基础接口

### GET `/` - 获取服务信息

获取服务的基本信息和支持的模板列表

**请求**

```bash
curl http://localhost:8000/
```

**响应**

```json
{
  "service": "TSC-Print-Middleware",
  "version": "3.0.0",
  "mode": "USB",
  "docs": "/docs",
  "health": "/health",
  "templates": [
    "single-text",
    "double-text",
    "qrcode-with-text",
    "barcode-with-text",
    "custom"
  ]
}
```

---

### GET `/health` - 健康检查

检查服务是否正常运行

**请求**

```bash
curl http://localhost:8000/health
```

**响应**

```json
{
  "status": "alive",
  "service": "tsc-print-middleware"
}
```

---

### POST `/test` - 测试打印机连接

测试 USB 打印机是否正常连接

**请求**

```bash
curl -X POST http://localhost:8000/test
```

**成功响应**

```json
{
  "status": "ok",
  "message": "USB打印机连接成功"
}
```

**失败响应** (503 Service Unavailable)

```json
{
  "detail": "USB打印机连接失败"
}
```

---

## 打印接口

### POST `/print` - 统一打印接口

所有打印任务都通过此接口完成，根据 `template` 参数选择不同的打印模式。

---

### 1. single-text - 单行文本

**用途**: 单行文本水平垂直居中打印

**打印效果**:

```
┌─────────────────────┐
│                     │
│   物料编号: A12345   │
│                     │
└─────────────────────┘
```

**请求体**

```json
{
  "template": "single-text",
  "print_list": [
    { "text": "物料编号: A12345" },
    { "text": "产品名称: 测试产品" }
  ]
}
```

**参数说明**

| 字段              | 类型   | 必填 | 说明                 |
| ----------------- | ------ | ---- | -------------------- |
| template          | string | 是   | 固定为 "single-text" |
| print_list        | array  | 是   | 打印数据列表         |
| print_list[].text | string | 是   | 文本内容             |

**响应**

```json
{
  "status": "ok",
  "message": "单行文本打印成功：2张标签"
}
```

**Python 示例**

```python
import requests

response = requests.post("http://localhost:8000/print", json={
    "template": "single-text",
    "print_list": [
        {"text": "物料编号: A12345"},
        {"text": "产品名称: 测试产品"}
    ]
})
print(response.json())
```

**cURL 示例**

```bash
curl -X POST http://localhost:8000/print \
  -H "Content-Type: application/json" \
  -d '{
    "template": "single-text",
    "print_list": [
      {"text": "物料编号: A12345"}
    ]
  }'
```

---

### 2. double-text - 双行文本

**用途**: 每张纸上下两行打印两个标签（节省纸张）

**打印效果**:

```
┌─────────────────────┐
│   第一行文本内容     │
├─────────────────────┤
│   第二行文本内容     │
└─────────────────────┘
```

**请求体**

```json
{
  "template": "double-text",
  "print_list": [
    { "text1": "物料A-盖子" },
    { "text2": "物料B-底座" },
    { "text1": "物料C-配件" }
  ]
}
```

**参数说明**

| 字段               | 类型   | 必填 | 说明                               |
| ------------------ | ------ | ---- | ---------------------------------- |
| template           | string | 是   | 固定为 "double-text"               |
| print_list         | array  | 是   | 打印数据列表                       |
| print_list[].text1 | string | 是   | 第一行文本                         |
| print_list[].text2 | string | 否   | 第二行文本（最后一张可能只有一行） |

**注意事项**:

- 系统会自动将连续两条数据打印在同一张纸的上下两行
- 如果数据数量为奇数，最后一张纸只打印一行

**响应**

```json
{
  "status": "ok",
  "message": "双行文本打印成功：3个标签（共2张纸）"
}
```

**Python 示例**

```python
import requests

response = requests.post("http://localhost:8000/print", json={
    "template": "double-text",
    "print_list": [
        {"text1": "物料A-盖子"},
        {"text2": "物料B-底座"},
        {"text1": "物料C-配件"}
    ]
})
print(response.json())
# 输出: "双行文本打印成功：3个标签（共2张纸）"
```

---

### 3. qrcode-with-text - 二维码+文本

**用途**: 二维码在上，文本在下，整体居中

**打印效果**:

```
┌─────────────────────┐
│    ████████████     │
│    ██ QR CODE ██    │
│    ████████████     │
│                     │
│   产品编号: 12345    │
└─────────────────────┘
```

**请求体**

```json
{
  "template": "qrcode-with-text",
  "print_list": [
    {
      "qrcode": "https://example.com/product/12345",
      "text": "产品编号: 12345"
    },
    {
      "qrcode": "https://example.com/product/67890",
      "text": "产品编号: 67890"
    }
  ]
}
```

**参数说明**

| 字段                | 类型   | 必填 | 说明                      |
| ------------------- | ------ | ---- | ------------------------- |
| template            | string | 是   | 固定为 "qrcode-with-text" |
| print_list          | array  | 是   | 打印数据列表              |
| print_list[].qrcode | string | 是   | 二维码内容（URL 或文本）  |
| print_list[].text   | string | 是   | 下方显示的文本            |

**响应**

```json
{
  "status": "ok",
  "message": "二维码标签打印成功：2张"
}
```

**Python 示例**

```python
import requests

response = requests.post("http://localhost:8000/print", json={
    "template": "qrcode-with-text",
    "print_list": [
        {
            "qrcode": "https://example.com/product/12345",
            "text": "产品编号: 12345"
        }
    ]
})
```

**JavaScript 示例**

```javascript
const axios = require("axios");

async function printQRCode() {
  const response = await axios.post("http://localhost:8000/print", {
    template: "qrcode-with-text",
    print_list: [
      {
        qrcode: "https://example.com/product/12345",
        text: "产品编号: 12345",
      },
    ],
  });
  console.log(response.data);
}
```

---

### 4. barcode-with-text - 条形码+文本

**用途**: 条形码在上，文本在下，整体居中

**打印效果**:

```
┌─────────────────────┐
│   ║║ ║║ ║║ ║║ ║║   │
│   ║║ ║║ ║║ ║║ ║║   │
│                     │
│  订单号: 1234567890  │
└─────────────────────┘
```

**请求体**

```json
{
  "template": "barcode-with-text",
  "print_list": [
    {
      "barcode": "1234567890",
      "text": "订单号: 1234567890"
    },
    {
      "barcode": "9876543210",
      "text": "订单号: 9876543210"
    }
  ]
}
```

**参数说明**

| 字段                 | 类型   | 必填 | 说明                       |
| -------------------- | ------ | ---- | -------------------------- |
| template             | string | 是   | 固定为 "barcode-with-text" |
| print_list           | array  | 是   | 打印数据列表               |
| print_list[].barcode | string | 是   | 条形码内容（数字或字母）   |
| print_list[].text    | string | 是   | 下方显示的文本             |

**响应**

```json
{
  "status": "ok",
  "message": "条形码标签打印成功：2张"
}
```

**Python 示例**

```python
import requests

response = requests.post("http://localhost:8000/print", json={
    "template": "barcode-with-text",
    "print_list": [
        {
            "barcode": "1234567890",
            "text": "订单号: 1234567890"
        }
    ]
})
```

---

### 5. custom - 完全自定义

**用途**: 高级用户完全控制布局和元素位置

**请求体**

```json
{
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
        "y": 700,
        "content": "123456789",
        "height": 80,
        "barcode_type": "128"
      }
    ]
  },
  "qty": 1
}
```

**参数说明**

| 字段            | 类型   | 必填 | 说明                   |
| --------------- | ------ | ---- | ---------------------- |
| template        | string | 是   | 固定为 "custom"        |
| layout          | object | 是   | 自定义布局对象         |
| layout.width    | number | 否   | 标签宽度(mm)，默认 100 |
| layout.height   | number | 否   | 标签高度(mm)，默认 80  |
| layout.elements | array  | 是   | 元素列表               |
| qty             | number | 否   | 打印数量，默认 1       |

**元素类型**

#### 文本元素

```json
{
  "type": "text",
  "x": 100, // X坐标 (dots)，必填
  "y": 100, // Y坐标 (dots)，必填
  "text": "文本内容", // 文本，必填
  "font_size": 48, // 字体大小 (12-120)，默认48
  "font_name": "宋体" // 字体名称，默认"宋体"
}
```

#### 二维码元素

```json
{
  "type": "qrcode",
  "x": 200, // X坐标 (dots)，必填
  "y": 200, // Y坐标 (dots)，必填
  "content": "二维码内容", // 内容，必填
  "size": 10 // 单元宽度 (1-10)，默认10
}
```

#### 条形码元素

```json
{
  "type": "barcode",
  "x": 100, // X坐标 (dots)，必填
  "y": 400, // Y坐标 (dots)，必填
  "content": "123456789", // 内容，必填
  "height": 80, // 高度 (30-300)，默认80
  "barcode_type": "128" // 类型，默认"128"
}
```

**坐标系统**

- 原点 (0, 0) 在左上角
- 单位: dots（点）
- 转换公式: `dots = mm × 11.81` (300 DPI)
- 示例: 100mm = 1181 dots

**响应**

```json
{
  "status": "ok",
  "message": "自定义布局打印成功：1张"
}
```

**Python 示例**

```python
import requests

response = requests.post("http://localhost:8000/print", json={
    "template": "custom",
    "layout": {
        "width": 100,
        "height": 80,
        "elements": [
            {
                "type": "text",
                "x": 100,
                "y": 100,
                "text": "库存盘点标签",
                "font_size": 56,
                "font_name": "宋体"
            },
            {
                "type": "qrcode",
                "x": 300,
                "y": 300,
                "content": "https://example.com/inventory/A12345",
                "size": 10
            },
            {
                "type": "text",
                "x": 200,
                "y": 650,
                "text": "编号: A12345",
                "font_size": 40
            }
        ]
    },
    "qty": 5  # 打印5张
})
```

---

## 错误处理

### HTTP 状态码

| 状态码 | 说明       | 场景                           |
| ------ | ---------- | ------------------------------ |
| 200    | 成功       | 打印任务完成                   |
| 400    | 请求错误   | 参数缺失、格式错误、模板不支持 |
| 500    | 服务器错误 | 打印命令执行失败、打印机异常   |
| 503    | 服务不可用 | USB 打印机连接失败             |

### 错误响应格式

```json
{
  "detail": "错误描述信息"
}
```

### 常见错误

#### 1. print_list 不能为空

```json
{
  "detail": "print_list不能为空"
}
```

**原因**: 预设模板需要提供 print_list 参数

**解决**: 确保 print_list 是非空数组

---

#### 2. 不支持的模板类型

```json
{
  "detail": "不支持的模板类型: xxx"
}
```

**原因**: template 参数值不在支持列表中

**解决**: 使用以下之一: single-text, double-text, qrcode-with-text, barcode-with-text, custom

---

#### 3. custom 模板需要提供 layout 参数

```json
{
  "detail": "custom模板需要提供layout参数"
}
```

**原因**: 使用 custom 模板但未提供 layout 对象

**解决**: 添加 layout 参数并包含 elements 数组

---

#### 4. USB 打印机连接失败

```json
{
  "detail": "USB打印机连接失败"
}
```

**原因**: 打印机未连接或驱动异常

**解决**:

- 检查打印机 USB 连接
- 确认打印机电源已开启
- 查看设备管理器是否识别打印机

---

## 代码示例

### Python 完整示例

```python
import requests

BASE_URL = "http://localhost:8000"

# 1. 健康检查
health = requests.get(f"{BASE_URL}/health")
print(health.json())

# 2. 测试打印机连接
test = requests.post(f"{BASE_URL}/test")
print(test.json())

# 3. 单行文本打印
single = requests.post(f"{BASE_URL}/print", json={
    "template": "single-text",
    "print_list": [
        {"text": "物料编号: A12345"}
    ]
})
print(single.json())

# 4. 双行文本打印
double = requests.post(f"{BASE_URL}/print", json={
    "template": "double-text",
    "print_list": [
        {"text1": "第一行"},
        {"text2": "第二行"}
    ]
})
print(double.json())

# 5. 二维码打印
qrcode = requests.post(f"{BASE_URL}/print", json={
    "template": "qrcode-with-text",
    "print_list": [
        {
            "qrcode": "https://example.com",
            "text": "扫码查看"
        }
    ]
})
print(qrcode.json())

# 6. 条形码打印
barcode = requests.post(f"{BASE_URL}/print", json={
    "template": "barcode-with-text",
    "print_list": [
        {
            "barcode": "1234567890",
            "text": "订单号: 1234567890"
        }
    ]
})
print(barcode.json())

# 7. 自定义布局打印
custom = requests.post(f"{BASE_URL}/print", json={
    "template": "custom",
    "layout": {
        "elements": [
            {
                "type": "text",
                "x": 100,
                "y": 100,
                "text": "标题",
                "font_size": 56
            },
            {
                "type": "qrcode",
                "x": 300,
                "y": 300,
                "content": "https://example.com",
                "size": 10
            }
        ]
    },
    "qty": 1
})
print(custom.json())
```

### JavaScript/Node.js 示例

```javascript
const axios = require("axios");

const BASE_URL = "http://localhost:8000";

async function printExamples() {
  try {
    // 1. 单行文本
    const single = await axios.post(`${BASE_URL}/print`, {
      template: "single-text",
      print_list: [{ text: "物料编号: A12345" }],
    });
    console.log(single.data);

    // 2. 二维码
    const qrcode = await axios.post(`${BASE_URL}/print`, {
      template: "qrcode-with-text",
      print_list: [
        {
          qrcode: "https://example.com",
          text: "扫码查看",
        },
      ],
    });
    console.log(qrcode.data);

    // 3. 自定义布局
    const custom = await axios.post(`${BASE_URL}/print`, {
      template: "custom",
      layout: {
        elements: [
          {
            type: "text",
            x: 100,
            y: 100,
            text: "标题",
            font_size: 56,
          },
          {
            type: "qrcode",
            x: 300,
            y: 300,
            content: "https://example.com",
            size: 10,
          },
        ],
      },
      qty: 1,
    });
    console.log(custom.data);
  } catch (error) {
    console.error("打印失败:", error.response?.data);
  }
}

printExamples();
```

---

## 技术支持

- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc
- **GitHub Issues**: [提交问题](https://github.com/你的用户名/TSC-Print-Middleware/issues)
- **讨论区**: [参与讨论](https://github.com/你的用户名/TSC-Print-Middleware/discussions)

---

**💡 提示**: 建议先使用 Swagger UI (http://localhost:8000/docs) 进行接口测试，它提供了交互式的 API 文档和测试功能。
