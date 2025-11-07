"""
TSC打印机测试脚本 - 支持中文打印
可以随意修改下面的打印内容进行测试
"""
import sys
import os
from printer import print_label, print_type1, print_type2, print_type3, print_calibration_border, calibrate_paper

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
        "data": {
            "type": 1,
            "print_list": [
                {"text": "cc测试拆箱物料1_盖子_1_1"},
                {"text": "【cc测试拆箱物料2】_底座_1_2"},
            ]
        }
    },
    {
        "name": "Type 2 - 二维码+文本（独占纸张）",
        "data": {
            "type": 2,
            "print_list": [
                {
                    "text": "sn：ODR2025102900030018001",
                    "qr_content": "ODR2025102900030018001"
                }
            ]
        }
    },
    {
        "name": "Type 3 - 6格批量二维码+文本（每张纸6个格子）",
        "data": {
            "type": 3,
            "print_list": [
                {"text": "GG2025111100001"},
                {"text": "GG2025111100002"},
                {"text": "GG2025111100003"},
                {"text": "GG2025111100004"},
                {"text": "GG2025111100005"},
                {"text": "GG2025111100006"}
            ]
        }
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
    
    # 判断打印类型（新格式：使用 data 字段）
    if 'data' in config and config['data'].get('type') == 1:
        # Type 1: 批量纯文本打印（上下两行）
        data = config['data']
        text_list = [item['text'] for item in data['print_list']]
        
        print(f"打印模式: Type 1 - 批量纯文本打印（上下两行）")
        print(f"API 请求数据: {data}")
        print(f"标签列表:")
        for i, text in enumerate(text_list, 1):
            print(f"  {i}. {text}")
        print(f"标签数量: {len(text_list)} 个")
        print(f"打印张数: {(len(text_list) + 1) // 2} 张")
        print(f"固定参数: 纸张=100mm×80mm, 字体=宋体56点")
        print()
        
        try:
            print_type1(text_list=text_list)
            print("✅ [成功] Type 1 批量打印命令已发送到USB打印机")
            return True
        except Exception as e:
            print(f"❌ [失败] {e}")
            return False
    
    elif 'data' in config and config['data'].get('type') == 2:
        # Type 2: 二维码+文本打印（独占纸张）
        data = config['data']
        
        print(f"打印模式: Type 2 - 二维码+文本打印（独占纸张）")
        print(f"API 请求数据: {data}")
        print(f"打印列表:")
        for i, item in enumerate(data['print_list'], 1):
            print(f"  {i}. 文本: {item['text']}, 二维码: {item['qr_content']}")
        print(f"打印数量: {len(data['print_list'])} 张")
        print(f"固定参数: 纸张=100mm×80mm, 字体=宋体48点, 二维码大小=从配置文件读取")
        print()
        
        try:
            # 批量打印（与 main.py 中的逻辑完全一致）
            for item in data['print_list']:
                print_type2(
                    qr_content=item['qr_content'],
                    text=item['text'],
                    qty=1
                )
            print("✅ [成功] Type 2 二维码+文本打印命令已发送到USB打印机")
            return True
        except Exception as e:
            print(f"❌ [失败] {e}")
            return False
    
    elif 'data' in config and config['data'].get('type') == 3:
        # Type 3: 6格批量二维码+文本打印（每张纸6个格子）
        data = config['data']
        data_list = [item['text'] for item in data['print_list']]
        
        print(f"打印模式: Type 3 - 6格批量二维码+文本打印")
        print(f"API 请求数据: {data}")
        print(f"标签列表:")
        for i, text in enumerate(data_list, 1):
            print(f"  {i}. {text}")
        print(f"标签数量: {len(data_list)} 个")
        print(f"打印张数: {(len(data_list) + 5) // 6} 张")
        print(f"固定参数: 纸张=100mm×80mm, 每格=50mm×26.67mm, 字体=宋体28点, 二维码大小=5")
        print(f"布局说明: 每张纸6个格子（3行×2列），每格左侧二维码+右侧文本")
        print()
        
        try:
            print_type3(data_list=data_list)
            print("✅ [成功] Type 3 6格批量打印命令已发送到USB打印机")
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

