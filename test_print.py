"""
TSC打印机测试脚本 - 支持中文打印
可以随意修改下面的打印内容进行测试
"""
import sys
import os
from printer import print_label, print_type1, print_type2, print_calibration_border, calibrate_paper

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
        "name": "校准1 - 打印区域校准（边框测试）",
        "type": "calibration",
        "description": "打印边框和角标记，检查打印是否从纸张开头正确开始",
        "qty": 1,
        "width": "100",
        "height": "80"
    },
    {
        "name": "校准2 - 纸张自动校准（间隙检测）",
        "type": "paper_calibration",
        "description": "让打印机自动检测标签间隙，调整打印位置（使用EOP命令）"
    },
    {
        "name": "Type 1 - 批量纯文本打印（上下两行）",
        "type": "type1",
        "text_list": [
            "cc测试拆箱物料1_盖子_1_1",
            "cc测试拆箱物料2_底座_1_2",
        ],
        "width": "100",
        "height": "80"
    },
    {
        "name": "Type 2 - 二维码+文本（独占纸张）",
        "type": "type2",
        "qr_content": "567890234567",
        "text": "sn：567890234567",
        "qty": 1,
        "width": "100",
        "height": "80",
        "qr_size": 12
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
    if config.get('type') == 'type1':
        # Type 1: 批量纯文本打印（上下两行）
        print(f"打印模式: Type 1 - 批量纯文本打印（上下两行）")
        print(f"标签列表:")
        for i, text in enumerate(config['text_list'], 1):
            print(f"  {i}. {text}")
        print(f"标签数量: {len(config['text_list'])} 个")
        print(f"打印张数: {(len(config['text_list']) + 1) // 2} 张")
        print(f"标签尺寸: {config['width']}mm x {config['height']}mm")
        print(f"固定参数: 字体=宋体56点")
        print()
        
        try:
            print_type1(
                text_list=config['text_list'],
                width=config['width'],
                height=config['height']
            )
            print("✅ [成功] Type 1 批量打印命令已发送到USB打印机")
            return True
        except Exception as e:
            print(f"❌ [失败] {e}")
            return False
    elif config.get('type') == 'type2':
        # Type 2: 二维码+文本打印（独占纸张）
        print(f"打印模式: Type 2 - 二维码+文本打印（独占纸张）")
        print(f"二维码内容: {config['qr_content']}")
        print(f"文本内容: {config['text']}")
        print(f"打印数量: {config['qty']}")
        print(f"二维码大小: {config['qr_size']}")
        print(f"标签尺寸: {config['width']}mm x {config['height']}mm")
        print(f"固定参数: 字体=宋体48点")
        print()
        
        try:
            print_type2(
                qr_content=config['qr_content'],
                text=config['text'],
                qty=config['qty'],
                width=config['width'],
                height=config['height'],
                qr_size=config['qr_size']
            )
            print("✅ [成功] Type 2 二维码+文本打印命令已发送到USB打印机")
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
    elif config.get('type') == 'paper_calibration':
        # 纸张自动校准
        print(f"打印模式: 纸张自动校准（间隙检测）")
        print(f"说明: {config.get('description', '')}")
        print()
        print("⚠️  注意:")
        print("  - 适用于有间隙的标签纸（标签之间有透明间隔）")
        print("  - 打印机会自动检测标签间隙并调整打印位置")
        print("  - 使用 EOP 命令进行校准，不会打印测试页")
        print("  - 建议在首次使用或更换纸张后执行")
        print()
        print("💡 如果您的纸张是连续纸（无间隙），请联系开发人员修改 GAP 设置")
        print()
        
        confirm = input("是否确认执行纸张校准? (y/n): ")
        if confirm.lower() != 'y':
            print("⚠️  已取消校准")
            return False
        
        try:
            print("⏳ 正在执行纸张校准...")
            success = calibrate_paper()
            if success:
                print("✅ [成功] 纸张校准完成，打印机已自动检测标签间隙")
                print()
                print("💡 提示: 校准完成后，请运行「校准1」检查打印位置是否正确")
                print("💡 提示: 然后可以测试 Type 1 或 Type 2 打印功能")
                return True
            else:
                print("❌ [失败] 纸张校准失败")
                return False
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

