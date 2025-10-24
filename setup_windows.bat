@echo off
chcp 65001 >nul
REM Windows环境自动安装脚本 - TSC-Print-Service

echo ========================================
echo 🚀 TSC-Print-Service Windows环境设置
echo ========================================
echo.

REM 1. 检查Python版本
echo 📦 步骤1: 检查Python版本...
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ❌ 未检测到Python！
    echo 请先安装Python 3.10-3.12: https://www.python.org/downloads/
    pause
    exit /b 1
)

for /f "tokens=2" %%i in ('python --version 2^>^&1') do set PYTHON_VERSION=%%i
echo ✅ 检测到Python版本: %PYTHON_VERSION%

REM 提取主版本号和次版本号
for /f "tokens=1,2 delims=." %%a in ("%PYTHON_VERSION%") do (
    set MAJOR=%%a
    set MINOR=%%b
)

if %MAJOR% LSS 3 (
    echo ❌ Python版本过低，需要3.10-3.12
    pause
    exit /b 1
)

if %MAJOR% EQU 3 (
    if %MINOR% LSS 10 (
        echo ⚠️  警告：Python 3.%MINOR% 可能不兼容，推荐3.10-3.12
    )
    if %MINOR% GTR 12 (
        echo ⚠️  警告：Python 3.%MINOR% 未经测试，推荐3.10-3.12
    )
)

REM 2. 创建虚拟环境
echo.
echo 🐍 步骤2: 创建Python虚拟环境...
if exist venv (
    echo ✅ 虚拟环境已存在
) else (
    echo 正在创建虚拟环境...
    python -m venv venv
    if %errorlevel% neq 0 (
        echo ❌ 创建虚拟环境失败
        pause
        exit /b 1
    )
    echo ✅ 虚拟环境已创建
)

REM 3. 激活虚拟环境
echo.
echo 📚 步骤3: 安装Python依赖...
call venv\Scripts\activate.bat
if %errorlevel% neq 0 (
    echo ❌ 激活虚拟环境失败
    pause
    exit /b 1
)

REM 4. 升级pip和wheel
echo 正在升级pip和wheel...
python -m pip install --upgrade pip wheel --quiet
if %errorlevel% neq 0 (
    echo ⚠️  pip升级失败，继续安装...
)

REM 5. 安装依赖
echo 正在安装项目依赖（可能需要几分钟）...
pip install -r requirements.txt
if %errorlevel% neq 0 (
    echo ❌ 依赖安装失败
    pause
    exit /b 1
)
echo ✅ 依赖安装完成

REM 6. 验证TSCLib
echo.
echo 🔍 步骤4: 验证TSCLib...
python -c "from tsclib import TSCPrinter; print('✅ TSCLib加载成功！')" 2>nul
if %errorlevel% neq 0 (
    echo ❌ TSCLib加载失败！
    echo.
    echo 常见解决方案：
    echo 1. 安装 Microsoft Visual C++ 2015-2022 Redistributable (x86)
    echo    下载地址: https://aka.ms/vs/17/release/vc_redist.x86.exe
    echo.
    echo 2. 重启电脑后重新运行此脚本
    echo.
    pause
    exit /b 1
)

REM 安装成功
echo.
echo ========================================
echo ✨ 安装完成！
echo ========================================
echo.
echo 下一步：
echo 1. 启动服务（双击）:     run.bat
echo 2. 或手动启动:           venv\Scripts\activate ^&^& python main.py
echo 3. 访问API文档:          http://localhost:8000/docs
echo.
echo 故障排查：
echo - 如果提示0x8007007e错误，安装VC++ 2015-2022运行库(x86)
echo - 确保打印机和电脑在同一局域网
echo ========================================
echo.
pause

