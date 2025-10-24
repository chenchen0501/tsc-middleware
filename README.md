# TSC-Print-Service

**"零驱动"局域网打印中间件 | macOS(M4)开发 ➜ Windows 部署**

## 快速开始

### macOS M4 开发环境

```bash
# 1. 安装Rosetta和x86_64 Homebrew（仅首次）
/usr/sbin/softwareupdate --install-rosetta --agree-to-license
arch -x86_64 /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"

# 2. 安装mono和libgdiplus
arch -x86_64 /usr/local/bin/brew install mono libgdiplus

# 3. 创建Python虚拟环境
python3 -m venv venv
source venv/bin/activate
pip install -U pip wheel

# 4. 安装依赖
pip install -r requirements.txt

# 5. 验证安装
python -c "from tsclib import TSCPrinter; print('✅ TSCLib加载成功')"
```

### 启动服务

```bash
# 开发模式（支持热重载）
uvicorn main:app --host 0.0.0.0 --port 8000 --reload

# 生产模式
uvicorn main:app --host 0.0.0.0 --port 8000
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

### 方式 1：自动安装（推荐）

双击运行 `setup_windows.bat`，脚本会自动：

- 检查 Python 版本（需要 3.10-3.12）
- 创建虚拟环境
- 安装所有依赖
- 验证 TSCLib
- 提示可能需要的 VC++运行库

安装完成后，双击 `run.bat` 启动服务

### 方式 2：手动安装

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

详见 `开发.md`

## 打印测试

### 方式 1：使用测试脚本（推荐）

**命令提示符 (CMD):**
```cmd
test.bat
```

**PowerShell:**
```powershell
.\test.ps1
```

**直接运行 (已激活虚拟环境):**
```bash
python test_print.py
```

测试脚本支持：
- ✅ 中文打印测试
- ✅ 英文打印测试  
- ✅ 中英文混合测试
- ✅ 交互式选择测试项

### 方式 2：编辑测试配置

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
  - 使用 `test.bat` 或 `test.ps1` 启动测试（已自动配置UTF-8编码）
  - 如果PowerShell仍有乱码，在PowerShell中执行：`$OutputEncoding = [System.Text.Encoding]::UTF8`
  - 确保打印机支持中文字体（推荐使用字体代码 "5" 或 "TSS24.BF2"）
