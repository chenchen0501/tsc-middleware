#!/bin/bash
# TSC打印机测试脚本 - macOS

# 设置mono和pythonnet环境变量
export MONO_GAC_PREFIX="/opt/homebrew"
export DYLD_LIBRARY_PATH="/opt/homebrew/lib:$DYLD_LIBRARY_PATH"
export PYTHONNET_RUNTIME=mono

# 激活虚拟环境
source venv/bin/activate

# 运行测试
echo "🧪 正在运行TSC打印机测试..."
echo ""
python test_print.py

