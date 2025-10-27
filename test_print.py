"""
TSC打印机测试脚本 - 支持中文打印
可以随意修改下面的打印内容进行测试
"""
import sys
import os
from printer import print_label, print_batch_labels, print_qrcode_with_text, print_calibration_border

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

# 打印内容配置（已改为USB模式，无需配置IP）
# 纸张区域：宽10cm（100mm）× 高8cm（80mm）
PRINT_CONFIGS = [
    {
        "name": "测试1 - 英文打印",
        "text": "AAAAAAAAAAAAAAAAAAAAAAAAAAAAAA",
        # "barcode": "JAVALY2024",
        "qty": 1,
        "width": "100",
        "height": "80"
    },
    {
        "name": "测试2 - 中文打印",
        "text": "哈哈哈哈哈哈哈哈哈哈哈哈哈哈哈哈哈哈",
        # "barcode": "CN2024",
        "qty": 1,
        "width": "100",
        "height": "80"
    },
    {
        "name": "测试3 - 中英文混合",
        "text": "基本粒子HHHHHHHHHHHHHHHHH",
        # "barcode": "MIX2024",
        "qty": 1,
        "width": "100",
        "height": "80"
    },
    {
        "name": "测试4 - 批量打印（上下两行）",
        "type": "batch",
        "text_list": [
            "cc测试拆箱物料1_盖子_1_1",
            "cc测试拆箱物料2_底座_1_2",
        ],
        "width": "100",
        "height": "80"
    },
    {
        "name": "测试5 - 二维码+文本",
        "type": "qrcode_text",
        "qr_content": "https://www.example.com/product/ABC123",
        "text": "Product-ABC123-2024",
        "qty": 1,
        "width": "100",
        "height": "80",
        "qr_size": 8
    },
    {
        "name": "测试6 - 打印区域校准（边框测试）",
        "type": "calibration",
        "description": "打印边框和角标记，检查打印是否从纸张开头正确开始",
        "qty": 1,
        "width": "100",
        "height": "80"
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
    print(f"打印机模式: USB")
    
    # 判断打印类型
    if config.get('type') == 'batch':
        # 批量打印
        print(f"打印模式: 批量打印（上下两行）")
        print(f"标签列表:")
        for i, text in enumerate(config['text_list'], 1):
            print(f"  {i}. {text}")
        print(f"标签数量: {len(config['text_list'])} 个")
        print(f"打印张数: {(len(config['text_list']) + 1) // 2} 张")
        print(f"标签尺寸: {config['width']}mm x {config['height']}mm")
        print()
        
        try:
            print_batch_labels(
                text_list=config['text_list'],
                width=config['width'],
                height=config['height']
            )
            print("✅ [成功] 批量打印命令已发送到USB打印机")
            return True
        except Exception as e:
            print(f"❌ [失败] {e}")
            return False
    elif config.get('type') == 'qrcode_text':
        # 二维码+文本打印
        print(f"打印模式: 二维码+文本")
        print(f"二维码内容: {config['qr_content']}")
        print(f"文本内容: {config['text']}")
        print(f"打印数量: {config['qty']}")
        print(f"二维码大小: {config['qr_size']}")
        print(f"标签尺寸: {config['width']}mm x {config['height']}mm")
        print()
        
        try:
            print_qrcode_with_text(
                qr_content=config['qr_content'],
                text=config['text'],
                qty=config['qty'],
                width=config['width'],
                height=config['height'],
                qr_size=config['qr_size']
            )
            print("✅ [成功] 二维码+文本打印命令已发送到USB打印机")
            return True
        except Exception as e:
            print(f"❌ [失败] {e}")
            return False
    elif config.get('type') == 'calibration':
        # 打印区域校准测试
        print(f"打印模式: 打印区域校准")
        print(f"说明: {config.get('description', '')}")
        print(f"打印数量: {config['qty']}")
        print(f"标签尺寸: {config['width']}mm x {config['height']}mm")
        print()
        print("📋 校准说明:")
        print("  - 会打印边框、四个角的坐标标记、中心十字线")
        print("  - 左上角标记为 START(0,0)，代表打印起始位置")
        print("  - 检查边框是否与纸张边缘对齐")
        print("  - 检查四个角标记是否在正确位置")
        print()
        
        try:
            print_calibration_border(
                qty=config['qty'],
                width=config['width'],
                height=config['height']
            )
            print("✅ [成功] 校准边框打印命令已发送到USB打印机")
            print()
            print("🔍 请检查打印结果:")
            print("  1. 边框是否从纸张开头正确开始")
            print("  2. 左上角 START(0,0) 标记位置是否正确")
            print("  3. 四个角的标记是否在纸张的四角")
            print("  4. 中心标记是否在纸张中心")
            return True
        except Exception as e:
            print(f"❌ [失败] {e}")
            return False
    else:
        # 单个打印
        print(f"文本内容: {config['text']}")
        print(f"条形码: {config.get('barcode', '无')}")
        print(f"打印数量: {config['qty']}")
        print(f"标签尺寸: {config['width']}mm x {config['height']}mm")
        print()
        
        try:
            print_label(
                text=config['text'],
                barcode=config.get('barcode', ''),
                qty=config['qty'],
                width=config['width'],
                height=config['height']
            )
            print("✅ [成功] 打印命令已发送到USB打印机")
            return True
        except Exception as e:
            print(f"❌ [失败] {e}")
            return False


def main():
    """主函数"""
    print("\n" + "="*50)
    print("  TSC打印机测试程序（USB模式）")
    print("="*50)
    print(f"\n📍 连接模式: USB")
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

