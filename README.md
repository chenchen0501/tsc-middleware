# TSC-Print-Service

**"零驱动"局域网打印中间件 | macOS(M4)开发 ➜ Windows 部署**

## 快速开始

### macOS M 芯片开发环境

```bash
# 1. 安装Rosetta（仅首次，M芯片Mac必需）
softwareupdate --install-rosetta --agree-to-license

# 2. 安装mono和mono-libgdiplus
brew install mono mono-libgdiplus

# 3. 创建Python虚拟环境
python3 -m venv venv
source venv/bin/activate
pip install -U pip

# 4. 安装依赖
pip install -r requirements.txt

# 5. 设置环境变量并验证
export MONO_GAC_PREFIX="/opt/homebrew"
export DYLD_LIBRARY_PATH="/opt/homebrew/lib:$DYLD_LIBRARY_PATH"
export PYTHONNET_RUNTIME=mono
python -c "from tsclib import TSCPrinter; print('✅ TSCLib加载成功')"
```

### 配置打印机 IP

**方法 1：修改配置文件（推荐）**

编辑 `config.py` 文件：

```python
PRINTER_IP = "192.168.1.100"  # 修改为你的打印机IP
```

**方法 2：使用环境变量**

```bash
export PRINTER_IP=192.168.1.200
```

### 启动服务

**macOS（使用启动脚本）:**

```bash
./start.sh
```

**或手动启动:**

```bash
# 设置环境变量
export MONO_GAC_PREFIX="/opt/homebrew"
export DYLD_LIBRARY_PATH="/opt/homebrew/lib:$DYLD_LIBRARY_PATH"
export PYTHONNET_RUNTIME=mono

# （可选）设置打印机IP
export PRINTER_IP=192.168.1.100

# 激活虚拟环境
source venv/bin/activate

# 开发模式（支持热重载）
uvicorn main:app --host 0.0.0.0 --port 8000 --reload
```

**Windows:**

```cmd
venv\Scripts\activate
python main.py
```

访问 http://localhost:8000/docs 查看交互式 API 文档

## API 接口

### 打印标签 `POST /print`

```json
{
  "ip": "192.168.1.100",
  "text": "Hello M4",
  "barcode": "1234567890",
  "qty": 1,
  "width": "50",
  "height": "30"
}
```

### 测试连接 `POST /test`

```json
{
  "ip": "192.168.1.100"
}
```

### 健康检查 `GET /health`

## Windows 部署

```cmd
# 1. 创建虚拟环境
python -m venv venv

# 2. 激活虚拟环境
venv\Scripts\activate

# 3. 安装依赖
pip install -r requirements.txt

# 4. 启动服务
python main.py
```

## 打印测试

### 使用测试脚本

**macOS（推荐）:**

```bash
./test.sh
```

**手动运行（需先设置环境变量）:**

```bash
# 设置环境变量
export MONO_GAC_PREFIX="/opt/homebrew"
export DYLD_LIBRARY_PATH="/opt/homebrew/lib:$DYLD_LIBRARY_PATH"
export PYTHONNET_RUNTIME=mono

# 激活虚拟环境
source venv/bin/activate

# 运行测试
python test_print.py
```

测试脚本支持：

- ✅ 中文打印测试
- ✅ 英文打印测试
- ✅ 中英文混合测试
- ✅ 交互式选择测试项

### 自定义测试配置

打开 `test_print.py`，修改 `PRINT_CONFIGS` 配置：

```python
PRINT_CONFIGS = [
    {
        "name": "自定义测试",
        "text": "你的文本内容",
        "barcode": "条形码内容",
        "qty": 1,
        "width": "100",
        "height": "90"
    },
]
```

## 故障排查

- **macOS**: 如果提示 `libgdiplus not found`，执行：

  ```bash
  export DYLD_LIBRARY_PATH=/usr/local/lib
  ```

- **Windows**: 如果提示 `0x8007007e`，安装 VC2015-2022 x86 运行库

- **连接失败**: ping 打印机 IP，确保在同一网络

- **中文乱码**:
  - 确保 Python 环境编码为 UTF-8
  - Windows 系统建议在 PowerShell 中执行：`$OutputEncoding = [System.Text.Encoding]::UTF8`
  - 确保打印机支持中文字体（推荐使用字体代码 "5" 或 "TSS24.BF2"）
