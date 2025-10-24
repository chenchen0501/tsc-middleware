@echo off
chcp 65001 >nul
echo ========================================
echo 🧪 启动TSC打印机测试程序
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

REM 激活虚拟环境并运行测试
call venv\Scripts\activate.bat
echo ✅ 虚拟环境已激活
echo.

python test_print.py

REM 测试结束后暂停
echo.
pause

