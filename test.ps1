# 设置控制台编码为UTF-8
[Console]::OutputEncoding = [System.Text.Encoding]::UTF8
$env:PYTHONIOENCODING = "utf-8"

Write-Host "========================================" -ForegroundColor Cyan
Write-Host "🧪 启动TSC打印机测试程序" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

# 检查虚拟环境
if (-not (Test-Path "venv")) {
    Write-Host "❌ 虚拟环境不存在！" -ForegroundColor Red
    Write-Host "请先运行 setup_windows.bat 进行安装" -ForegroundColor Yellow
    Write-Host ""
    pause
    exit 1
}

# 激活虚拟环境并运行测试
& "venv\Scripts\Activate.ps1"
Write-Host "✅ 虚拟环境已激活" -ForegroundColor Green
Write-Host ""

python test_print.py

# 测试结束后暂停
Write-Host ""
pause

