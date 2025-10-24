# TSC 打印服务 API 接口文档

## 📋 目录

- [服务信息](#服务信息)
- [基础接口](#基础接口)
  - [获取服务信息](#获取服务信息)
  - [健康检查](#健康检查)
  - [测试打印机连接](#测试打印机连接)
- [打印接口](#打印接口)
  - [打印文本标签](#打印文本标签)
  - [打印二维码标签](#打印二维码标签)
  - [批量打印标签](#批量打印标签)
- [错误码说明](#错误码说明)

---

## 服务信息

- **服务名称**: TSC-Print-Service
- **版本**: 1.0.0
- **描述**: 零驱动局域网打印中间件 | macOS 开发 ➜ Windows 部署
- **默认端口**: 8000
- **默认打印机 IP**: 192.168.1.100（可在 config.py 或环境变量中修改）
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
  "version": "1.0.0",
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

### 测试打印机连接

测试与指定打印机的网络连接

**请求**

```
POST /test
Content-Type: application/json
```

**请求参数**

| 参数名 | 类型   | 必填 | 默认值        | 说明                   | 示例            |
| ------ | ------ | ---- | ------------- | ---------------------- | --------------- |
| ip     | string | 否   | 配置的默认 IP | 打印机 IP 地址（可选） | "192.168.1.100" |

**请求示例 1：使用默认 IP**

```json
{}
```

**请求示例 2：指定 IP**

```json
{
  "ip": "192.168.1.100"
}
```

**成功响应**

```json
{
  "status": "ok",
  "message": "打印机 192.168.1.100 连接正常"
}
```

**失败响应**

- **状态码**: 503 (Service Unavailable)
- **响应体**:

```json
{
  "detail": "无法连接到打印机 192.168.1.100"
}
```

---

## 打印接口

### 打印文本标签

打印包含文字和条形码的标签（条形码可选）

**请求**

```
POST /print
Content-Type: application/json
```

**请求参数**

| 参数名  | 类型    | 必填 | 默认值        | 说明                           | 示例                           |
| ------- | ------- | ---- | ------------- | ------------------------------ | ------------------------------ |
| ip      | string  | 否   | 配置的默认 IP | 打印机 IP 地址（可选）         | "192.168.1.100"                |
| text    | string  | 是   | -             | 标签文本内容（支持中文）       | "cc 测试拆箱物料 1\_盖子\_1_1" |
| barcode | string  | 否   | ""            | 条形码内容（不传则不打印条码） | "1234567890"                   |
| qty     | integer | 否   | 1             | 打印数量（1-100）              | 1                              |
| width   | string  | 否   | "100"         | 标签宽度(mm)                   | "100"                          |
| height  | string  | 否   | "90"          | 标签高度(mm)                   | "90"                           |

**请求示例 1：使用默认 IP，只打印文字**

```json
{
  "text": "cc测试拆箱物料1_盖子_1_1"
}
```

**请求示例 2：指定 IP，打印文字+条形码**

```json
{
  "ip": "192.168.1.100",
  "text": "产品编号：12345",
  "barcode": "1234567890",
  "qty": 2
}
```

**成功响应**

```json
{
  "status": "ok",
  "message": "成功发送1张标签到打印机 192.168.1.100"
}
```

**失败响应**

- **状态码**: 500 (Internal Server Error)
- **响应体**:

```json
{
  "detail": "打印失败: [具体错误信息]"
}
```

---

### 打印二维码标签

打印包含二维码的标签

**请求**

```
POST /print/qrcode
Content-Type: application/json
```

**请求参数**

| 参数名  | 类型    | 必填 | 默认值        | 说明                     | 示例                      |
| ------- | ------- | ---- | ------------- | ------------------------ | ------------------------- |
| ip      | string  | 否   | 配置的默认 IP | 打印机 IP 地址（可选）   | "192.168.1.100"           |
| content | string  | 是   | -             | 二维码内容（URL 或文本） | "https://www.example.com" |
| text    | string  | 否   | ""            | 标签附加文本（可选）     | "扫码访问"                |
| qty     | integer | 否   | 1             | 打印数量（1-100）        | 1                         |
| width   | string  | 否   | "100"         | 标签宽度(mm)             | "100"                     |
| height  | string  | 否   | "90"          | 标签高度(mm)             | "90"                      |
| qr_size | integer | 否   | 8             | 二维码大小（1-10）       | 8                         |

**请求示例**

```json
{
  "content": "https://www.example.com",
  "text": "扫码访问官网",
  "qty": 1,
  "qr_size": 8
}
```

**成功响应**

```json
{
  "status": "ok",
  "message": "成功发送1张二维码标签到打印机 192.168.1.100"
}
```

**失败响应**

- **状态码**: 500 (Internal Server Error)
- **响应体**:

```json
{
  "detail": "打印失败: [具体错误信息]"
}
```

---

### 批量打印标签

批量打印多个文本标签，每张纸上下两行打印两个标签

**特点**：

- 10cm × 9cm 纸张
- 每张纸上下排列打印两个标签
- 自动分组：每两个文本为一组打印在同一张纸上
- 如果是奇数个标签，最后一张纸只打印一个

**请求**

```
POST /print/batch
Content-Type: application/json
```

**请求参数**

| 参数名    | 类型          | 必填 | 默认值        | 说明                   | 示例            |
| --------- | ------------- | ---- | ------------- | ---------------------- | --------------- |
| ip        | string        | 否   | 配置的默认 IP | 打印机 IP 地址（可选） | "192.168.1.100" |
| text_list | array[string] | 是   | -             | 要打印的文本列表       | 见下方示例      |
| width     | string        | 否   | "100"         | 标签宽度(mm)           | "100"           |
| height    | string        | 否   | "90"          | 标签高度(mm)           | "90"            |

**请求示例**

```json
{
  "text_list": [
    "cc测试拆箱物料1_盖子_1_1",
    "cc测试拆箱物料2_底座_1_2",
    "cc测试拆箱物料3_配件_1_3",
    "cc测试拆箱物料4_螺丝_1_4",
    "cc测试拆箱物料5_垫片_1_5"
  ]
}
```

**打印说明**：

- 上述 5 个文本会打印在 3 张纸上
  - 第 1 张纸：上方"物料 1"，下方"物料 2"
  - 第 2 张纸：上方"物料 3"，下方"物料 4"
  - 第 3 张纸：上方"物料 5"

**成功响应**

```json
{
  "status": "ok",
  "message": "成功发送5个标签（共3张纸）到打印机 192.168.1.100"
}
```

**失败响应**

- **状态码**: 400 (Bad Request) - 文本列表为空

```json
{
  "detail": "文本列表不能为空"
}
```

- **状态码**: 500 (Internal Server Error) - 打印失败

```json
{
  "detail": "批量打印失败: [具体错误信息]"
}
```

---

## 错误码说明

| HTTP 状态码 | 说明       | 可能原因                           |
| ----------- | ---------- | ---------------------------------- |
| 200         | 成功       | 请求处理成功                       |
| 400         | 请求错误   | 参数验证失败、文本列表为空等       |
| 500         | 服务器错误 | 打印机通信失败、打印命令执行失败等 |
| 503         | 服务不可用 | 无法连接到打印机                   |

---

## 使用示例

### Python 示例

```python
import requests

# 服务地址
BASE_URL = "http://localhost:8000"

# 1. 测试连接（使用默认IP）
response = requests.post(f"{BASE_URL}/test", json={})
print(response.json())

# 2. 打印文本标签（使用默认IP）
response = requests.post(f"{BASE_URL}/print", json={
    "text": "cc测试拆箱物料1_盖子_1_1"
})
print(response.json())

# 3. 批量打印（使用默认IP）
response = requests.post(f"{BASE_URL}/print/batch", json={
    "text_list": [
        "cc测试拆箱物料1_盖子_1_1",
        "cc测试拆箱物料2_底座_1_2",
        "cc测试拆箱物料3_配件_1_3"
    ]
})
print(response.json())

# 4. 指定IP打印
response = requests.post(f"{BASE_URL}/print", json={
    "ip": "192.168.1.200",  # 使用不同的打印机
    "text": "特殊打印机标签"
})
print(response.json())
```

### cURL 示例

```bash
# 1. 健康检查
curl http://localhost:8000/health

# 2. 测试连接（使用默认IP）
curl -X POST http://localhost:8000/test \
  -H "Content-Type: application/json" \
  -d '{}'

# 3. 打印文本标签（使用默认IP）
curl -X POST http://localhost:8000/print \
  -H "Content-Type: application/json" \
  -d '{
    "text": "cc测试拆箱物料1_盖子_1_1"
  }'

# 4. 批量打印（使用默认IP）
curl -X POST http://localhost:8000/print/batch \
  -H "Content-Type: application/json" \
  -d '{
    "text_list": [
      "cc测试拆箱物料1_盖子_1_1",
      "cc测试拆箱物料2_底座_1_2"
    ]
  }'
```

### JavaScript/Node.js 示例

```javascript
const axios = require("axios");

const BASE_URL = "http://localhost:8000";

// 批量打印（使用默认IP）
async function batchPrint() {
  try {
    const response = await axios.post(`${BASE_URL}/print/batch`, {
      text_list: [
        "cc测试拆箱物料1_盖子_1_1",
        "cc测试拆箱物料2_底座_1_2",
        "cc测试拆箱物料3_配件_1_3",
      ],
    });
    console.log(response.data);
  } catch (error) {
    console.error("打印失败:", error.response?.data);
  }
}

// 打印单个标签（使用默认IP）
async function printLabel() {
  try {
    const response = await axios.post(`${BASE_URL}/print`, {
      text: "cc测试拆箱物料1_盖子_1_1",
    });
    console.log(response.data);
  } catch (error) {
    console.error("打印失败:", error.response?.data);
  }
}

batchPrint();
printLabel();
```

---

## 注意事项

1. **打印机 IP 配置**:

   - 默认打印机 IP 为 `192.168.1.100`
   - 可以通过修改 `config.py` 文件中的 `PRINTER_IP` 来更改默认 IP
   - 也可以通过环境变量 `PRINTER_IP` 设置，例如：`export PRINTER_IP=192.168.1.200`
   - API 调用时可以传入 `ip` 参数临时覆盖默认 IP

2. **网络连接**: 确保打印机和服务器在同一局域网内

3. **打印机端口**: TSC 打印机默认使用 9100 端口

4. **中文支持**: 使用 Windows 系统字体（宋体）打印中文

5. **字体大小**: 当前字体高度为 56 点，可根据需要调整

6. **标签尺寸**: 默认 100mm × 90mm，可根据实际标签纸调整

7. **批量打印**: 自动将文本列表分组，每两个文本打印在一张纸上

---

## 技术支持

如有问题，请查看：

- Swagger API 文档: http://localhost:8000/docs
- ReDoc 文档: http://localhost:8000/redoc
