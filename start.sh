#!/bin/bash
# TSC打印服务启动脚本 - macOS

# 设置mono和pythonnet环境变量
export MONO_GAC_PREFIX="/opt/homebrew"
export DYLD_LIBRARY_PATH="/opt/homebrew/lib:$DYLD_LIBRARY_PATH"
export PYTHONNET_RUNTIME=mono

# 激活虚拟环境
source venv/bin/activate

# 启动服务
echo "🚀 正在启动TSC打印服务..."
echo "📍 访问 http://localhost:8000/docs 查看API文档"
echo ""
uvicorn main:app --host 0.0.0.0 --port 8000 --reload

