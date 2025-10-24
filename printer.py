"""
TSC打印机核心模块（跨平台）
支持USB和网络打印机
"""
from tsclib import TSCPrinter


def print_label(
    ip: str,
    text: str,
    barcode: str = "",
    qty: int = 1,
    width: str = "100",
    height: str = "90"
):
    """
    打印标签
    
    Args:
        ip: 打印机IP地址（如：192.168.1.100）
        text: 标签文本
        barcode: 条形码内容（可选，默认不打印条码）
        qty: 打印数量
        width: 标签宽度(mm)
        height: 标签高度(mm)
    """
    p = TSCPrinter()
    try:
        # 打开网络端口（9100是TSC默认端口）
        p.open_port(f"{ip}:9100")
        
        # 使用原始TSPL命令以支持中文
        p.send_command("CLS")
        p.send_command(f"SIZE {width} mm, {height} mm")
        p.send_command("GAP 2 mm, 0 mm")
        p.send_command("SPEED 4")
        p.send_command("DENSITY 10")
        p.send_command("DIRECTION 1")
        
        # 打印文本（使用UTF-8编码支持中文）
        p.send_command_utf8(f'TEXT 150,30,"5",0,1,1,"{text}"')
        
        # 打印条形码（如果提供）
        if barcode:
            p.send_command(f'BARCODE 150,150,"128",80,1,0,2,2,"{barcode}"')
        
        # 执行打印
        p.send_command(f"PRINT {qty},1")
    finally:
        # 确保关闭端口
        p.close_port()


def print_batch_labels(
    ip: str,
    text_list: list[str],
    width: str = "100",
    height: str = "90"
):
    """
    批量打印标签（10cm×9cm纸张，每张上下两行打印两个标签）
    
    Args:
        ip: 打印机IP地址（如：192.168.1.100）
        text_list: 要打印的文本列表，如 ["cc测试拆箱物料1_盖子_1_1", "cc测试拆箱物料2_底座_1_2"]
        width: 标签宽度(mm)，默认100mm（10cm）
        height: 标签高度(mm)，默认90mm（9cm）
    """
    p = TSCPrinter()
    try:
        # 打开网络端口
        p.open_port(f"{ip}:9100")
        
        # 每两个文本为一组，打印在一张纸上（上下两行）
        for i in range(0, len(text_list), 2):
            # 清除缓冲区
            p.send_command("CLS")
            
            # 设置标签尺寸
            p.send_command(f"SIZE {width} mm, {height} mm")
            p.send_command("GAP 0 mm, 0 mm")  # 减小标签间隔
            p.send_command("SPEED 4")
            p.send_command("DENSITY 10")
            p.send_command("DIRECTION 1")
            p.send_command("SET TEAR ON")  # 撕纸模式
            p.send_command("CODEPAGE UTF-8")  # 设置UTF-8编码
            
            # 打印第一行（上方）- 左上角位置
            first_text = text_list[i]
            p.send_command_utf8(f'TEXT 30,80,"TSS24.BF2",0,1,1,"{first_text}"')
            
            # 打印第二行（下方，如果存在）
            if i + 1 < len(text_list):
                second_text = text_list[i + 1]
                p.send_command_utf8(f'TEXT 30,360,"TSS24.BF2",0,1,1,"{second_text}"')
            
            # 执行打印一张
            p.send_command("PRINT 1,1")
            
    finally:
        # 确保关闭端口
        p.close_port()


def print_qrcode(
    ip: str,
    content: str,
    text: str = "",
    qty: int = 1,
    width: str = "100",
    height: str = "90",
    qr_size: int = 8
):
    """
    打印二维码标签
    
    Args:
        ip: 打印机IP地址（如：192.168.1.100）
        content: 二维码内容（URL或文本）
        text: 标签文本（可选）
        qty: 打印数量
        width: 标签宽度(mm)
        height: 标签高度(mm)
        qr_size: 二维码单元宽度(1-10，数字越大二维码越大)
    """
    p = TSCPrinter()
    try:
        # 打开网络端口
        p.open_port(f"{ip}:9100")
        
        # 清除缓冲区
        p.send_command("CLS")
        
        # 设置标签尺寸
        p.send_command(f"SIZE {width} mm, {height} mm")
        p.send_command("GAP 2 mm, 0 mm")
        
        # 设置打印参数
        p.send_command("SPEED 4")
        p.send_command("DENSITY 10")
        p.send_command("DIRECTION 1")
        
        # 打印文本（如果提供）
        if text:
            # 使用UTF-8编码发送中文文本
            p.send_command_utf8(f'TEXT 250,30,"5",0,1,1,"{text}"')
            qr_y = 150  # 二维码位置居中
        else:
            qr_y = 100
        
        # 打印二维码（居中位置）
        # QRCODE x,y,纠错等级,单元宽度,模式,旋转,"内容"
        # 二维码内容使用UTF-8编码
        p.send_command_utf8(f'QRCODE 250,{qr_y},H,{qr_size},A,0,"{content}"')
        
        # 执行打印
        p.send_command(f"PRINT {qty},1")
        
    finally:
        p.close_port()


def test_connection(ip: str) -> bool:
    """
    测试打印机连接
    
    Args:
        ip: 打印机IP地址
        
    Returns:
        bool: 连接成功返回True
    """
    p = TSCPrinter()
    try:
        p.open_port(f"{ip}:9100")
        p.close_port()
        return True
    except Exception:
        return False

