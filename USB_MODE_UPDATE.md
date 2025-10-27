# USB 模式更新说明

## 📌 更新概述

项目已从**网络连接模式**全面切换为 **USB 连接模式**。

**版本**: 1.0.0 → 2.0.0

**原因**: `TSCSDK.node_usb` 类不支持网络连接（使用 `IP:端口` 参数会报错），需统一使用 USB 模式。

---

## 🔧 修改内容

### 1. **printer.py** ✅

所有打印函数改为使用 `p.open_port(0)` (USB 模式):

- `print_label()` - 打印文本标签
- `print_batch_labels()` - 批量打印
- `print_qrcode()` - 打印二维码
- `print_qrcode_with_text()` - 二维码+文本
- `test_connection()` - 测试连接

**关键改动**:

```python
# 旧代码（网络模式）
p.open_port(f"{ip}:9100")

# 新代码（USB模式）
p.open_port(0)  # 0 表示第一个USB打印机
```

### 2. **main.py** ✅

FastAPI 服务全面更新:

- 移除所有 API 模型中的 `ip` 参数
- 更新所有 API 文档描述为 USB 模式
- 版本号更新为 2.0.0
- 服务描述更新为"零驱动 USB 打印中间件"

**API 变化**:

```python
# 旧请求格式
POST /print
{
  "ip": "192.168.1.100",  # ❌ 已移除
  "text": "Hello"
}

# 新请求格式
POST /print
{
  "text": "Hello"  # ✅ 直接使用USB
}
```

### 3. **test_print.py** ✅

测试脚本更新:

- 移除 `PRINTER_IP` 配置变量
- 所有打印函数调用去除 `ip` 参数
- 更新提示信息为 USB 模式

### 4. **config.py** ✅

配置文件简化:

- 移除 `PRINTER_IP` 配置
- 添加 USB 模式说明

---

## 📋 使用方法

### 前提条件

1. ✅ 打印机通过 **USB** 连接到电脑
2. ✅ 打印机电源已打开
3. ✅ 已安装打印机驱动

### 测试打印

**Windows:**

```cmd
venv\Scripts\activate
python test_print.py
```

**macOS:**

```bash
./test.sh
python test_print.py
```

### 启动 API 服务

**Windows:**

```cmd
venv\Scripts\activate
python main.py
```

**macOS:**

```bash
./start.sh
```

访问: http://localhost:8000/docs

### API 调用示例

**1. 打印文本标签**

```bash
curl -X POST http://localhost:8000/print \
  -H "Content-Type: application/json" \
  -d '{
    "text": "Hello USB Printer"
  }'
```

**2. 批量打印**

```bash
curl -X POST http://localhost:8000/print/batch \
  -H "Content-Type: application/json" \
  -d '{
    "text_list": ["标签1", "标签2", "标签3"]
  }'
```

**3. 测试连接**

```bash
curl -X POST http://localhost:8000/test
```

---

## 🔍 诊断工具

### 列出可用打印机

```bash
python list_printers.py
```

显示所有 USB 打印机的驱动名称和设备信息。

### 全面诊断测试

```bash
python diagnose.py
```

测试多种连接方式，帮助排查问题。

---

## ⚠️ 注意事项

1. **网络模式已不可用**

   - 所有网络连接代码已移除
   - 如需网络打印，需使用其他库或 SDK

2. **API 兼容性**

   - 旧版 API 请求中的 `ip` 参数将被忽略（如果前端还在传）
   - 建议更新前端代码，移除 IP 相关参数

3. **多打印机支持**

   - 当前默认连接第一个 USB 打印机 (`port_index=0`)
   - 如需支持多打印机，可扩展 `open_port()` 参数

4. **驱动要求**
   - 确保安装了正确的 TSC 打印机驱动
   - Windows 需要 .NET Framework
   - macOS 需要 Mono 运行时

---

## 🐛 故障排查

### 问题 1: 打印机连接失败

**症状**: `CallSite.Target` 或 `openport` 错误

**解决方案**:

1. 检查打印机 USB 连接
2. 确认打印机电源已打开
3. 运行 `python list_printers.py` 检查是否识别到打印机
4. 重新安装打印机驱动

### 问题 2: 找不到打印机

**症状**: `list_printers()` 返回空列表

**解决方案**:

1. 检查 USB 线缆连接
2. 重启打印机
3. 在设备管理器中确认打印机状态
4. 尝试更换 USB 端口

### 问题 3: 中文乱码

**症状**: 打印出的中文显示为乱码

**解决方案**:

1. 确保系统已安装"宋体"字体
2. 打印机支持中文字体
3. 使用 `print_text_windows_font()` 而非 `send_command()`

---

## 📊 技术细节

### open_port() 参数说明

根据 `tsclib` 文档:

- `p.open_port(0)` - 连接第一个 USB 打印机
- `p.open_port(1)` - 连接第二个 USB 打印机
- `p.open_port("TSC TTP-247")` - 使用驱动名称连接
- `p.open_port("192.168.1.100:9100")` - ❌ 不支持（会报错）

### TSCSDK.node_usb 限制

- 此类专为 USB 连接设计
- 不支持网络连接参数
- 传入 IP 字符串会导致 .NET 动态调用错误

---

## 📞 支持

如有问题，请查看：

- 诊断工具: `python diagnose.py`
- 打印机列表: `python list_printers.py`
- API 文档: http://localhost:8000/docs

---

**更新日期**: 2025-10-27  
**版本**: 2.0.0  
**模式**: USB Only
