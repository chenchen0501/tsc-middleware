@echo off
chcp 65001 >nul
echo ========================================
echo 🚀 启动TSC打印服务...
echo ========================================
echo.

REM 检查虚拟环境
if not exist venv (
    echo ❌ 虚拟环境不存在！
    echo 请先运行 setup_windows.bat 进行安装
    echo.
    pause
    exit /b 1
)

REM 激活虚拟环境并启动服务
call venv\Scripts\activate.bat
echo ✅ 虚拟环境已激活
echo.
echo 服务地址: http://localhost:8000
echo API文档:  http://localhost:8000/docs
echo.
echo 按 Ctrl+C 停止服务
echo ========================================
echo.

python main.py

REM 如果服务异常退出，保持窗口打开以查看错误
if %errorlevel% neq 0 (
    echo.
    echo ❌ 服务启动失败！错误代码: %errorlevel%
    echo.
    pause
)

