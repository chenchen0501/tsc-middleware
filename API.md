# TSC 打印服务 API 接口文档

## 📋 目录

- [服务信息](#服务信息)
- [基础接口](#基础接口)
  - [获取服务信息](#获取服务信息)
  - [健康检查](#健康检查)
- [打印接口](#打印接口)
  - [统一打印接口](#统一打印接口)
- [错误码说明](#错误码说明)

---

## 服务信息

- **服务名称**: TSC-Print-Service
- **版本**: 3.0.0
- **描述**: 零驱动 USB 打印中间件 | Windows 部署 | USB 连接模式
- **默认端口**: 8000
- **纸张规格**: 10cm × 8cm (100mm × 80mm)
- **连接方式**: USB（不使用网络 IP）
- **跨域支持**: 已启用 CORS，支持所有源访问
- **API 文档**: http://localhost:8000/docs (Swagger UI)

---

## 基础接口

### 获取服务信息

获取服务的基本信息

**请求**

```
GET /
```

**响应示例**

```json
{
  "service": "TSC-Print-Service",
  "version": "3.0.0",
  "mode": "USB",
  "docs": "/docs",
  "health": "/health"
}
```

---

### 健康检查

检查服务是否正常运行

**请求**

```
GET /health
```

**响应示例**

```json
{
  "status": "alive",
  "service": "tsc-print"
}
```

---

## 打印接口

### 统一打印接口

通过 `type` 参数区分不同的打印模式，所有打印任务都通过此接口完成。

**请求**

```
POST /print
Content-Type: application/json
```

**打印类型说明**

| type | 名称                | 说明                                 |
| ---- | ------------------- | ------------------------------------ |
| 1    | 批量纯文本打印      | 每张纸上下两行打印两个标签，每行居中 |
| 2    | 批量二维码+文本打印 | 每个二维码独占一张纸，整体居中       |

**通用参数说明**

| 参数名     | 类型          | 必填 | 说明                                           |
| ---------- | ------------- | ---- | ---------------------------------------------- |
| type       | integer       | 是   | 打印类型：1=纯文本批量, 2=二维码批量           |
| print_list | array[object] | 是   | 打印项列表，每个对象包含 text（和 qr_content） |

**重要提示**：所有打印参数（width、height、qr_size）已根据 type 固定，用户无需传递。

---

#### Type 1: 批量纯文本打印

每张纸上下两行打印两个标签

**print_list 对象结构**

| 字段名 | 类型   | 必填 | 说明     | 示例     |
| ------ | ------ | ---- | -------- | -------- |
| text   | string | 是   | 文本内容 | "物料 1" |

**请求示例**

```json
{
  "type": 1,
  "print_list": [
    { "text": "cc测试拆箱物料1_盖子_1_1" },
    { "text": "cc测试拆箱物料2_底座_1_2" },
    { "text": "cc测试拆箱物料3_配件_1_3" }
  ]
}
```

**打印说明**：

- 上述 3 个文本会打印在 2 张纸上
  - 第 1 张纸：上方"物料 1"，下方"物料 2"
  - 第 2 张纸：上方"物料 3"
- **固定参数**：
  - 纸张尺寸: 100mm × 80mm
  - 字体: 宋体 56 点
  - 边距: 10 dots (约 0.85mm)
  - 布局: 上下两行分别水平垂直居中

**成功响应**

```json
{
  "status": "ok",
  "message": "批量打印成功：3个标签（共2张纸）"
}
```

**失败响应**

- **状态码**: 400 (Bad Request) - 参数错误

```json
{
  "detail": "print_list参数不能为空"
}
```

---

#### Type 2: 批量二维码+文本打印

每个二维码独占一张纸

**print_list 对象结构**

| 字段名     | 类型   | 必填 | 说明                     | 示例                                     |
| ---------- | ------ | ---- | ------------------------ | ---------------------------------------- |
| text       | string | 是   | 文本内容                 | "Product-ABC123-2024"                    |
| qr_content | string | 是   | 二维码内容（URL 或文本） | "https://www.example.com/product/ABC123" |

**请求示例**

```json
{
  "type": 2,
  "print_list": [
    {
      "text": "Product-ABC123-2024",
      "qr_content": "https://www.example.com/product/ABC123"
    },
    {
      "text": "Product-DEF456-2024",
      "qr_content": "https://www.example.com/product/DEF456"
    }
  ]
}
```

**打印说明**：

- 每个二维码+文本独占一张纸
- 上述 2 个对象会打印 2 张纸
- **固定参数**：
  - 纸张尺寸: 100mm × 80mm
  - 字体: 宋体 48 点
  - 二维码大小: 10 (单元宽度，最大值)
  - 二维码与文本间距: 24 dots (约 2mm)
  - 边距: 10 dots (约 0.85mm)
  - 布局: 二维码和文本中心对齐，整体在纸张居中

**成功响应**

```json
{
  "status": "ok",
  "message": "二维码批量打印成功：2张标签"
}
```

**失败响应**

- **状态码**: 400 (Bad Request) - 参数错误

```json
{
  "detail": "print_list参数不能为空"
}
```

```json
{
  "detail": "type=2时，print_list中第1个对象的qr_content不能为空"
}
```

---

## 错误码说明

| HTTP 状态码 | 说明       | 可能原因                                    |
| ----------- | ---------- | ------------------------------------------- |
| 200         | 成功       | 请求处理成功                                |
| 400         | 请求错误   | type 参数错误、必需参数缺失、参数验证失败等 |
| 500         | 服务器错误 | 打印机 USB 连接失败、打印命令执行失败等     |

---

## 使用示例

### Python 示例

```python
import requests

# 服务地址
BASE_URL = "http://localhost:8000"

# 1. 健康检查
response = requests.get(f"{BASE_URL}/health")
print(response.json())

# 2. 批量纯文本打印（type=1）
response = requests.post(f"{BASE_URL}/print", json={
    "type": 1,
    "print_list": [
        {"text": "cc测试拆箱物料1_盖子_1_1"},
        {"text": "cc测试拆箱物料2_底座_1_2"},
        {"text": "cc测试拆箱物料3_配件_1_3"}
    ]
})
print(response.json())
# 输出: {"status": "ok", "message": "批量打印成功：3个标签（共2张纸）"}

# 3. 批量二维码+文本打印（type=2）
response = requests.post(f"{BASE_URL}/print", json={
    "type": 2,
    "print_list": [
        {
            "text": "Product-ABC123-2024",
            "qr_content": "https://www.example.com/product/ABC123"
        },
        {
            "text": "Product-DEF456-2024",
            "qr_content": "https://www.example.com/product/DEF456"
        }
    ]
})
print(response.json())
# 输出: {"status": "ok", "message": "二维码批量打印成功：2张标签"}
```

### cURL 示例

```bash
# 1. 健康检查
curl http://localhost:8000/health

# 2. 批量纯文本打印（type=1）
curl -X POST http://localhost:8000/print \
  -H "Content-Type: application/json" \
  -d '{
    "type": 1,
    "print_list": [
      {"text": "cc测试拆箱物料1_盖子_1_1"},
      {"text": "cc测试拆箱物料2_底座_1_2"}
    ]
  }'

# 3. 批量二维码+文本打印（type=2）
curl -X POST http://localhost:8000/print \
  -H "Content-Type: application/json" \
  -d '{
    "type": 2,
    "print_list": [
      {
        "text": "Product-ABC123-2024",
        "qr_content": "https://www.example.com/product/ABC123"
      },
      {
        "text": "Product-DEF456-2024",
        "qr_content": "https://www.example.com/product/DEF456"
      }
    ]
  }'
```

### JavaScript/Node.js 示例

```javascript
const axios = require("axios");

const BASE_URL = "http://localhost:8000";

// 批量纯文本打印（type=1）
async function batchTextPrint() {
  try {
    const response = await axios.post(`${BASE_URL}/print`, {
      type: 1,
      print_list: [
        { text: "cc测试拆箱物料1_盖子_1_1" },
        { text: "cc测试拆箱物料2_底座_1_2" },
        { text: "cc测试拆箱物料3_配件_1_3" },
      ],
    });
    console.log(response.data);
  } catch (error) {
    console.error("打印失败:", error.response?.data);
  }
}

// 批量二维码+文本打印（type=2）
async function batchQrcodePrint() {
  try {
    const response = await axios.post(`${BASE_URL}/print`, {
      type: 2,
      print_list: [
        {
          text: "Product-ABC123-2024",
          qr_content: "https://www.example.com/product/ABC123",
        },
        {
          text: "Product-DEF456-2024",
          qr_content: "https://www.example.com/product/DEF456",
        },
      ],
    });
    console.log(response.data);
  } catch (error) {
    console.error("打印失败:", error.response?.data);
  }
}

batchTextPrint();
batchQrcodePrint();
```

---

## 注意事项

1. **连接方式**: 使用 USB 连接打印机，不需要配置网络 IP 地址

2. **打印机型号**: TTE-344 (300 DPI)

3. **纸张规格**: 10cm × 8cm (100mm × 80mm)

4. **中文支持**: 使用 Windows 系统字体（宋体）打印中文

5. **固定参数**: 所有打印参数已根据 type 固定，用户无需传递

   - type=1: width=100mm, height=80mm
   - type=2: width=100mm, height=80mm, qr_size=10

6. **type=1 批量打印**: 自动将文本列表分组，每两个文本打印在一张纸的上下两行

7. **type=2 批量打印**: 每个二维码+文本独占一张纸，适合需要单独撕下的场景

8. **参数结构**: 统一使用 `print_list` 数组，每个元素都是对象，包含 `text` 字段（type=2 还需要 `qr_content` 字段）

9. **跨域访问（CORS）**:
   - 已启用 CORS 中间件，允许所有源（`*`）访问
   - 生产环境建议在 `main.py` 中修改 `allow_origins` 为具体的前端域名
   - 示例：`allow_origins=["https://yourdomain.com", "http://localhost:3000"]`

---

## 技术支持

如有问题，请查看：

- Swagger API 文档: http://localhost:8000/docs
- ReDoc 文档: http://localhost:8000/redoc
