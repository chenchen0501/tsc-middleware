#!/bin/bash
# macOS M4 开发环境自动安装脚本

echo "🚀 TSC-Print-Service M4开发环境设置"
echo "======================================"

# 检查是否是M4 Mac
if [[ $(uname -m) != "arm64" ]]; then
    echo "⚠️  警告：当前不是ARM架构，可能不需要Rosetta"
fi

# 1. 安装Rosetta
echo ""
echo "📦 步骤1: 检查Rosetta..."
if ! /usr/bin/pgrep -q oahd; then
    echo "正在安装Rosetta（需要管理员密码）..."
    /usr/sbin/softwareupdate --install-rosetta --agree-to-license
else
    echo "✅ Rosetta已安装"
fi

# 2. 检查x86_64 Homebrew
echo ""
echo "📦 步骤2: 检查x86_64 Homebrew..."
if [ ! -f "/usr/local/bin/brew" ]; then
    echo "正在安装x86_64版本的Homebrew..."
    arch -x86_64 /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
else
    echo "✅ x86_64 Homebrew已安装"
fi

# 3. 安装mono和libgdiplus
echo ""
echo "📦 步骤3: 安装mono和libgdiplus..."
arch -x86_64 /usr/local/bin/brew install mono libgdiplus

# 4. 创建Python虚拟环境
echo ""
echo "🐍 步骤4: 创建Python虚拟环境..."
if [ ! -d "venv" ]; then
    python3 -m venv venv
    echo "✅ 虚拟环境已创建"
else
    echo "✅ 虚拟环境已存在"
fi

# 5. 激活虚拟环境并安装依赖
echo ""
echo "📚 步骤5: 安装Python依赖..."
source venv/bin/activate
pip install -U pip wheel
pip install -r requirements.txt

# 6. 验证安装
echo ""
echo "🔍 步骤6: 验证TSCLib..."
python -c "from tsclib import TSCPrinter; print('✅ TSCLib加载成功！')" 2>&1

if [ $? -eq 0 ]; then
    echo ""
    echo "======================================"
    echo "✨ 安装完成！"
    echo ""
    echo "下一步："
    echo "1. 激活虚拟环境: source venv/bin/activate"
    echo "2. 启动服务: uvicorn main:app --host 0.0.0.0 --port 8000 --reload"
    echo "3. 访问API文档: http://localhost:8000/docs"
    echo "======================================"
else
    echo ""
    echo "❌ 安装出现问题，请检查错误信息"
    echo ""
    echo "常见解决方案："
    echo "- 确保已安装Python 3.10或更高版本"
    echo "- 如果提示libgdiplus错误，运行："
    echo "  export DYLD_LIBRARY_PATH=/usr/local/lib"
fi

