"""
测试不同的QRCODE命令格式，找出正确的格式

此脚本会打印2张测试标签，每张纸上有4个二维码（2×2布局）
请用手机扫描每个二维码，看哪个能被正确识别
"""
import logging
from tsclib import TSCPrinter
from config import DEFAULT_WIDTH, DEFAULT_HEIGHT, DPI_RATIO

# 配置日志
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

# 测试用的二维码内容（简单数字，容易识别）
TEST_QR_CONTENT = "123456789"

# 测试用的不同QRCODE命令格式
QRCODE_FORMATS = [
    {
        "name": "格式1: 基本格式（无model参数）",
        "command": f'QRCODE 200,200,H,12,A,0,"{TEST_QR_CONTENT}"',
        "description": "QRCODE x,y,ECC,size,mode,rotation,\"data\""
    },
    {
        "name": "格式2: 带M1模型",
        "command": f'QRCODE 200,200,H,12,A,0,M1,"{TEST_QR_CONTENT}"',
        "description": "QRCODE x,y,ECC,size,mode,rotation,M1,\"data\""
    },
    {
        "name": "格式3: 带M2模型",
        "command": f'QRCODE 200,200,H,12,A,0,M2,"{TEST_QR_CONTENT}"',
        "description": "QRCODE x,y,ECC,size,mode,rotation,M2,\"data\""
    },
    {
        "name": "格式4: 带M1模型和s7掩码",
        "command": f'QRCODE 200,200,H,12,A,0,M1,s7,"{TEST_QR_CONTENT}"',
        "description": "QRCODE x,y,ECC,size,mode,rotation,M1,mask,\"data\""
    },
    {
        "name": "格式5: 带M2模型和s7掩码",
        "command": f'QRCODE 200,200,H,12,A,0,M2,s7,"{TEST_QR_CONTENT}"',
        "description": "QRCODE x,y,ECC,size,mode,rotation,M2,mask,\"data\""
    },
    {
        "name": "格式6: 错误纠正级别改为M",
        "command": f'QRCODE 200,200,M,12,A,0,M2,"{TEST_QR_CONTENT}"',
        "description": "QRCODE x,y,M,size,mode,rotation,M2,\"data\""
    },
    {
        "name": "格式7: 更大的尺寸（size=15）",
        "command": f'QRCODE 200,200,H,15,A,0,M2,"{TEST_QR_CONTENT}"',
        "description": "QRCODE x,y,ECC,15,mode,rotation,M2,\"data\""
    },
    {
        "name": "格式8: 手动模式（M）",
        "command": f'QRCODE 200,200,H,12,M,0,M2,"{TEST_QR_CONTENT}"',
        "description": "QRCODE x,y,ECC,size,M,rotation,M2,\"data\""
    },
]


def print_batch_qrcodes(page_num: int, formats_batch: list):
    """
    在一张纸上打印4个测试二维码（2×2布局）
    
    Args:
        page_num: 页码（1或2）
        formats_batch: 包含4个格式信息的列表
    """
    p = TSCPrinter()
    try:
        logging.info(f"\n{'='*60}")
        logging.info(f"打印第 {page_num} 张测试纸（包含4个测试二维码）")
        logging.info(f"{'='*60}")
        
        # 打开USB端口
        p.open_port(0)
        
        # 清除缓冲区
        p.send_command("CLS")
        
        # 设置标签尺寸
        p.send_command(f"SIZE {DEFAULT_WIDTH} mm, {DEFAULT_HEIGHT} mm")
        
        # 设置间隙
        p.send_command("GAP 3 mm, 0 mm")
        
        # 设置方向
        p.send_command("DIRECTION 0")
        
        # 设置参考点
        p.send_command("REFERENCE 0,0")
        
        # 设置速度和浓度
        p.send_command("SPEED 4")
        p.send_command("DENSITY 12")
        
        # 关闭撕离模式
        p.send_command("SET TEAR OFF")
        p.send_command("SET PEEL OFF")
        
        # 计算布局（2×2，每张纸4个二维码）
        width_dots = int(float(DEFAULT_WIDTH) * DPI_RATIO)
        height_dots = int(float(DEFAULT_HEIGHT) * DPI_RATIO)
        
        # 分成4个区域：左上、右上、左下、右下
        half_width = width_dots // 2
        half_height = height_dots // 2
        
        # 每个区域的边距和尺寸
        margin_x = 30
        margin_y = 30
        qr_size = 8  # 二维码单元尺寸（适中，确保可识别）
        
        # 定义4个位置（左上、右上、左下、右下）
        positions = [
            {"x": margin_x, "y": margin_y},  # 左上
            {"x": half_width + margin_x, "y": margin_y},  # 右上
            {"x": margin_x, "y": half_height + margin_y},  # 左下
            {"x": half_width + margin_x, "y": half_height + margin_y},  # 右下
        ]
        
        # 打印4个二维码
        for i, format_info in enumerate(formats_batch):
            pos = positions[i]
            test_num = (page_num - 1) * 4 + i + 1  # 全局测试编号
            
            logging.info(f"  测试 {test_num}: {format_info['name']}")
            
            # 打印测试编号
            p.print_text_windows_font(
                x=pos["x"],
                y=pos["y"],
                font_height=24,
                rotation=0,
                font_style=1,  # Bold
                font_underline=0,
                font_face_name="Arial",
                text=f"#{test_num}"
            )
            
            # 打印格式名称（简短版本）
            format_short = format_info['name'].split(':')[1].strip()[:12]
            p.print_text_windows_font(
                x=pos["x"],
                y=pos["y"] + 30,
                font_height=16,
                rotation=0,
                font_style=0,
                font_underline=0,
                font_face_name="Arial",
                text=format_short
            )
            
            # 计算二维码位置（在文字下方）
            qr_x = pos["x"] + 60
            qr_y = pos["y"] + 70
            
            # 发送二维码命令（替换命令中的坐标）
            qr_cmd = format_info['command'].replace('200,200', f'{qr_x},{qr_y}')
            # 调整二维码尺寸（统一为qr_size）
            qr_cmd = qr_cmd.replace(',12,', f',{qr_size},').replace(',15,', f',{qr_size},')
            
            logging.info(f"    命令: {qr_cmd}")
            p.send_command(qr_cmd)
        
        # 执行打印
        p.send_command("PRINT 1,1")
        
        logging.info(f"✅ 第 {page_num} 张测试纸打印命令已发送")
        
    except Exception as e:
        logging.error(f"❌ 第 {page_num} 张测试纸打印失败: {e}")
        import traceback
        traceback.print_exc()
    finally:
        p.close_port()


def main():
    """主函数"""
    print("\n" + "="*60)
    print("  TSC 打印机 QRCODE 命令格式测试")
    print("="*60)
    print(f"\n测试内容: {TEST_QR_CONTENT}")
    print(f"测试格式: {len(QRCODE_FORMATS)} 种")
    print(f"打印张数: 2 张（每张纸4个二维码，2×2布局）")
    print("\n布局说明：")
    print("  每张纸分为4个区域：")
    print("  ┌─────────┬─────────┐")
    print("  │  #1/#5  │  #2/#6  │  第1张纸: 测试1-4")
    print("  ├─────────┼─────────┤  第2张纸: 测试5-8")
    print("  │  #3/#7  │  #4/#8  │")
    print("  └─────────┴─────────┘")
    print("\n使用方法：")
    print("1. 按回车开始打印2张测试纸")
    print("2. 打印完成后，用手机扫描每个二维码")
    print("3. 记录下能成功识别的测试编号（#1-#8）")
    print("4. 根据结果确定正确的QRCODE命令格式")
    print("\n" + "="*60)
    
    try:
        input("\n按回车键开始测试...")
        
        # 分成2批，每批4个格式
        batch_size = 4
        total_pages = (len(QRCODE_FORMATS) + batch_size - 1) // batch_size
        
        for page in range(total_pages):
            start_idx = page * batch_size
            end_idx = min(start_idx + batch_size, len(QRCODE_FORMATS))
            formats_batch = QRCODE_FORMATS[start_idx:end_idx]
            
            print(f"\n{'='*60}")
            print(f"准备打印第 {page + 1}/{total_pages} 张测试纸...")
            print(f"包含测试 #{start_idx + 1} 到 #{end_idx}")
            print(f"{'='*60}\n")
            
            print_batch_qrcodes(page + 1, formats_batch)
            
            # 打印间隔
            if page < total_pages - 1:
                import time
                time.sleep(3)
                print(f"\n等待3秒后打印下一张...\n")
        
        print("\n" + "="*60)
        print(f"✅ 所有测试完成！共打印 2 张测试纸，{len(QRCODE_FORMATS)} 个测试二维码")
        print("="*60)
        print("\n请用手机扫描每个二维码，记录能识别的编号：")
        print("\n第1张纸：")
        for i in range(4):
            print(f"  #{i+1}: {QRCODE_FORMATS[i]['name']}")
        print("\n第2张纸：")
        for i in range(4, 8):
            print(f"  #{i+1}: {QRCODE_FORMATS[i]['name']}")
        print("\n识别结果将帮助确定正确的QRCODE命令格式")
        print("详见 QRCODE测试指南.md 的「根据测试结果修改代码」部分\n")
        
    except KeyboardInterrupt:
        print("\n\n👋 用户取消操作")
    except Exception as e:
        print(f"\n❌ 发生错误: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()

