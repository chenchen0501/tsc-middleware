"""
TSC打印机测试脚本 - 支持中文打印
可以随意修改下面的打印内容进行测试
"""
import sys
import os
from printer import print_label

# Windows编码设置 - 修复中文乱码
if sys.platform == 'win32':
    # 设置控制台代码页为UTF-8
    os.system('chcp 65001 >nul 2>&1')
    # 设置环境变量
    os.environ['PYTHONIOENCODING'] = 'utf-8'

# 设置输出编码
if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')
if hasattr(sys.stderr, 'reconfigure'):
    sys.stderr.reconfigure(encoding='utf-8')

# ========================================
# 📝 配置区域 - 请根据需要修改以下内容
# ========================================

# 打印机IP地址
PRINTER_IP = "192.168.1.100"

# 打印内容配置
PRINT_CONFIGS = [
    {
        "name": "测试1 - 英文打印",
        "text": "AAAAAAAAAAAAAAAAAAAAAAAAAAAAAA",
        "barcode": "JAVALY2024",
        "qty": 1,
        "width": "100",
        "height": "90"
    },
    {
        "name": "测试2 - 中文打印",
        "text": "哈哈哈哈哈哈哈哈哈哈哈哈哈哈哈哈哈哈",
        "barcode": "CN2024",
        "qty": 1,
        "width": "100",
        "height": "90"
    },
    {
        "name": "测试3 - 中英文混合",
        "text": "基本粒子HHHHHHHHHHHHHHHHH",
        "barcode": "MIX2024",
        "qty": 1,
        "width": "100",
        "height": "90"
    },
]

# ========================================
# 执行测试
# ========================================

def run_test(config):
    """运行单个打印测试"""
    print(f"\n{'='*50}")
    print(f"🖨️  {config['name']}")
    print(f"{'='*50}")
    print(f"打印机IP: {PRINTER_IP}")
    print(f"文本内容: {config['text']}")
    print(f"条形码: {config['barcode']}")
    print(f"打印数量: {config['qty']}")
    print(f"标签尺寸: {config['width']}mm x {config['height']}mm")
    print()
    
    try:
        print_label(
            ip=PRINTER_IP,
            text=config['text'],
            barcode=config['barcode'],
            qty=config['qty'],
            width=config['width'],
            height=config['height']
        )
        print("✅ [成功] 打印命令已发送")
        return True
    except Exception as e:
        print(f"❌ [失败] {e}")
        return False


def main():
    """主函数"""
    print("\n" + "="*50)
    print("  TSC打印机测试程序")
    print("="*50)
    print(f"\n📍 目标打印机: {PRINTER_IP}")
    print(f"📋 测试任务数: {len(PRINT_CONFIGS)}")
    
    # 询问用户要执行哪个测试
    print("\n请选择要执行的测试：")
    for i, config in enumerate(PRINT_CONFIGS, 1):
        print(f"  {i}. {config['name']}")
    print(f"  {len(PRINT_CONFIGS) + 1}. 执行所有测试")
    print("  0. 退出")
    
    try:
        choice = input("\n请输入选项 (0-{}): ".format(len(PRINT_CONFIGS) + 1))
        choice = int(choice)
        
        if choice == 0:
            print("\n👋 已取消测试")
            return
        elif choice == len(PRINT_CONFIGS) + 1:
            # 执行所有测试
            success_count = 0
            for config in PRINT_CONFIGS:
                if run_test(config):
                    success_count += 1
                input("\n按回车键继续下一个测试...")
            
            print(f"\n{'='*50}")
            print(f"测试完成: {success_count}/{len(PRINT_CONFIGS)} 成功")
            print(f"{'='*50}")
        elif 1 <= choice <= len(PRINT_CONFIGS):
            # 执行单个测试
            run_test(PRINT_CONFIGS[choice - 1])
        else:
            print("\n❌ 无效的选项")
    except ValueError:
        print("\n❌ 请输入有效的数字")
    except KeyboardInterrupt:
        print("\n\n👋 用户取消操作")
    except Exception as e:
        print(f"\n❌ 发生错误: {e}")


if __name__ == "__main__":
    main()

