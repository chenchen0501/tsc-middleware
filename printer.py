"""
TSC打印机核心模块（跨平台）
支持USB连接（已改为使用USB模式，不再使用网络连接）
"""
import logging
from tsclib import TSCPrinter
from config import DEFAULT_WIDTH, DEFAULT_HEIGHT

# 配置日志
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")


def print_label(
    ip: str = "",
    text: str = "",
    barcode: str = "",
    qty: int = 1,
    width: str = None,
    height: str = None
):
    """
    打印标签
    
    Args:
        ip: 打印机IP地址（保留用于API兼容性，实际使用USB连接）
        text: 标签文本
        barcode: 条形码内容（可选，默认不打印条码）
        qty: 打印数量
        width: 标签宽度(mm)，默认使用config中的配置（10cm）
        height: 标签高度(mm)，默认使用config中的配置（8cm）
    """
    # 使用配置文件中的默认值
    if width is None:
        width = DEFAULT_WIDTH
    if height is None:
        height = DEFAULT_HEIGHT
    
    p = TSCPrinter()
    try:
        # 打开USB端口（参数0表示第一个USB打印机）
        logging.info("使用 USB 连接打印机...")
        p.open_port(0)
        
        # 清除缓冲区
        p.send_command("CLS")
        
        # 设置标签尺寸
        p.send_command(f"SIZE {width} mm, {height} mm")
        p.send_command("GAP 2 mm, 0 mm")
        p.send_command("SPEED 4")
        p.send_command("DENSITY 10")
        p.send_command("DIRECTION 1")
        
        # 打印文本（使用Windows字体支持中文）
        p.print_text_windows_font(
            x=50,
            y=200,
            font_height=56,  # 增大字体
            rotation=0,
            font_style=0,
            font_underline=0,
            font_face_name="宋体",  # 使用宋体支持中文
            text=text
        )
        
        # 打印条形码（如果提供）
        if barcode:
            p.send_command(f'BARCODE 150,150,"128",80,1,0,2,2,"{barcode}"')
        
        # 执行打印
        p.send_command(f"PRINT {qty},1")
    finally:
        # 确保关闭端口
        p.close_port()


def print_batch_labels(
    ip: str = "",
    text_list: list[str] = None,
    width: str = None,
    height: str = None
):
    """
    批量打印标签（每张上下两行打印两个标签）
    
    Args:
        ip: 打印机IP地址（保留用于API兼容性，实际使用USB连接）
        text_list: 要打印的文本列表，如 ["cc测试拆箱物料1_盖子_1_1", "cc测试拆箱物料2_底座_1_2"]
        width: 标签宽度(mm)，默认使用config中的配置（10cm）
        height: 标签高度(mm)，默认使用config中的配置（8cm）
    """
    if text_list is None:
        text_list = []
    
    # 使用配置文件中的默认值
    if width is None:
        width = DEFAULT_WIDTH
    if height is None:
        height = DEFAULT_HEIGHT
    
    p = TSCPrinter()
    try:
        # 打开USB端口（参数0表示第一个USB打印机）
        logging.info("使用 USB 连接打印机...")
        p.open_port(0)
        
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
            
            # 打印第一行（上方）- 使用Windows字体支持中文
            first_text = text_list[i]
            p.print_text_windows_font(
                x=50,
                y=80,
                font_height=56,  # 增大字体
                rotation=0,
                font_style=0,
                font_underline=0,
                font_face_name="宋体",
                text=first_text
            )
            
            # 打印第二行（下方，如果存在）
            if i + 1 < len(text_list):
                second_text = text_list[i + 1]
                p.print_text_windows_font(
                    x=50,
                    y=400,
                    font_height=56,  # 增大字体
                    rotation=0,
                    font_style=0,
                    font_underline=0,
                    font_face_name="宋体",
                    text=second_text
                )
            
            # 执行打印一张
            p.send_command("PRINT 1,1")
            
    finally:
        # 确保关闭端口
        p.close_port()


def print_qrcode(
    ip: str = "",
    content: str = "",
    text: str = "",
    qty: int = 1,
    width: str = None,
    height: str = None,
    qr_size: int = 8
):
    """
    打印二维码标签
    
    Args:
        ip: 打印机IP地址（保留用于API兼容性，实际使用USB连接）
        content: 二维码内容（URL或文本）
        text: 标签文本（可选）
        qty: 打印数量
        width: 标签宽度(mm)，默认使用config中的配置（10cm）
        height: 标签高度(mm)，默认使用config中的配置（8cm）
        qr_size: 二维码单元宽度(1-10，数字越大二维码越大)
    """
    # 使用配置文件中的默认值
    if width is None:
        width = DEFAULT_WIDTH
    if height is None:
        height = DEFAULT_HEIGHT
    
    p = TSCPrinter()
    try:
        # 打开USB端口（参数0表示第一个USB打印机）
        logging.info("使用 USB 连接打印机...")
        p.open_port(0)
        
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


def print_qrcode_with_text(
    ip: str = "",
    qr_content: str = "",
    text: str = "",
    qty: int = 1,
    width: str = None,
    height: str = None,
    qr_size: int = 8
):
    """
    打印二维码+文本标签（二维码在上方，文本在下方）
    
    Args:
        ip: 打印机IP地址（保留用于API兼容性，实际使用USB连接）
        qr_content: 二维码内容（URL或文本）
        text: 下方显示的文本（支持中文、英文、数字）
        qty: 打印数量
        width: 标签宽度(mm)，默认使用config中的配置（10cm）
        height: 标签高度(mm)，默认使用config中的配置（8cm）
        qr_size: 二维码单元宽度(1-10，数字越大二维码越大)
    """
    # 使用配置文件中的默认值
    if width is None:
        width = DEFAULT_WIDTH
    if height is None:
        height = DEFAULT_HEIGHT
    
    p = TSCPrinter()
    try:
        # 打开USB端口（参数0表示第一个USB打印机）
        logging.info("使用 USB 连接打印机...")
        p.open_port(0)
        
        # 清除缓冲区
        p.send_command("CLS")
        
        # 设置标签尺寸
        p.send_command(f"SIZE {width} mm, {height} mm")
        p.send_command("GAP 0 mm, 0 mm")
        
        # 设置打印参数
        p.send_command("SPEED 4")
        p.send_command("DENSITY 10")
        p.send_command("DIRECTION 1")
        
        # 打印二维码（上方位置）
        p.send_command_utf8(f'QRCODE 200,80,H,{qr_size},A,0,"{qr_content}"')
        
        # 打印文本（下方位置）- 使用Windows字体支持中英文
        p.print_text_windows_font(
            x=50,
            y=450,
            font_height=48,
            rotation=0,
            font_style=0,
            font_underline=0,
            font_face_name="宋体",
            text=text
        )
        
        # 执行打印
        p.send_command(f"PRINT {qty},1")
        
    finally:
        p.close_port()


def test_connection(ip: str = "") -> bool:
    """
    测试打印机连接
    
    Args:
        ip: 打印机IP地址（保留用于API兼容性，实际使用USB连接）
        
    Returns:
        bool: 连接成功返回True
    """
    p = TSCPrinter()
    try:
        logging.info("测试 USB 连接...")
        p.open_port(0)
        p.close_port()
        return True
    except Exception:
        return False


def print_calibration_border(
    qty: int = 1,
    width: str = None,
    height: str = None
):
    """
    打印校准边框和标记，用于检查打印区域是否从纸张开头正确开始
    
    会在标签的四个角和中心打印标记，以及边框线，帮助判断打印位置
    
    Args:
        qty: 打印数量
        width: 标签宽度(mm)，默认使用config中的配置（10cm）
        height: 标签高度(mm)，默认使用config中的配置（8cm）
    """
    # 使用配置文件中的默认值
    if width is None:
        width = DEFAULT_WIDTH
    if height is None:
        height = DEFAULT_HEIGHT
    
    p = TSCPrinter()
    try:
        # 打开USB端口
        logging.info("使用 USB 连接打印机...")
        p.open_port(0)
        
        # 清除缓冲区
        p.send_command("CLS")
        
        # 设置标签尺寸
        p.send_command(f"SIZE {width} mm, {height} mm")
        p.send_command("GAP 0 mm, 0 mm")
        p.send_command("SPEED 4")
        p.send_command("DENSITY 10")
        p.send_command("DIRECTION 1")
        
        # 转换为dots（假设200DPI: 1mm ≈ 8 dots）
        width_dots = int(float(width) * 8)
        height_dots = int(float(height) * 8)
        
        # 打印外边框（矩形）
        # BOX x_start, y_start, x_end, y_end, line_thickness
        border_thickness = 3
        p.send_command(f"BOX 10,10,{width_dots-10},{height_dots-10},{border_thickness}")
        
        # 打印四个角的标记文字
        # 左上角
        p.print_text_windows_font(
            x=20, y=30,
            font_height=32,
            rotation=0,
            font_style=0,
            font_underline=0,
            font_face_name="Arial",
            text="START(0,0)"
        )
        
        # 右上角
        p.print_text_windows_font(
            x=width_dots-150, y=30,
            font_height=32,
            rotation=0,
            font_style=0,
            font_underline=0,
            font_face_name="Arial",
            text=f"({width}mm,0)"
        )
        
        # 左下角
        p.print_text_windows_font(
            x=20, y=height_dots-60,
            font_height=32,
            rotation=0,
            font_style=0,
            font_underline=0,
            font_face_name="Arial",
            text=f"(0,{height}mm)"
        )
        
        # 右下角
        p.print_text_windows_font(
            x=width_dots-150, y=height_dots-60,
            font_height=32,
            rotation=0,
            font_style=0,
            font_underline=0,
            font_face_name="Arial",
            text=f"({width},{height}mm)"
        )
        
        # 中心标记
        center_x = width_dots // 2 - 60
        center_y = height_dots // 2 - 20
        p.print_text_windows_font(
            x=center_x, y=center_y,
            font_height=40,
            rotation=0,
            font_style=1,  # Bold
            font_underline=0,
            font_face_name="Arial",
            text="CENTER"
        )
        
        # 打印中心十字线
        cross_size = 40
        # 横线
        p.send_command(f"BAR {width_dots//2 - cross_size},{height_dots//2},{cross_size*2},2")
        # 竖线
        p.send_command(f"BAR {width_dots//2},{height_dots//2 - cross_size},2,{cross_size*2}")
        
        # 打印顶部标题
        p.print_text_windows_font(
            x=width_dots//2 - 100, y=height_dots//2 + 40,
            font_height=28,
            rotation=0,
            font_style=0,
            font_underline=0,
            font_face_name="宋体",
            text="打印区域校准测试"
        )
        
        # 打印尺寸信息
        p.print_text_windows_font(
            x=width_dots//2 - 80, y=height_dots//2 + 80,
            font_height=24,
            rotation=0,
            font_style=0,
            font_underline=0,
            font_face_name="Arial",
            text=f"Size: {width}mm x {height}mm"
        )
        
        # 执行打印
        p.send_command(f"PRINT {qty},1")
        
    finally:
        # 确保关闭端口
        p.close_port()

