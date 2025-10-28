"""
TSC打印机核心模块（跨平台）
支持USB连接（已改为使用USB模式，不再使用网络连接）
"""
import logging
from tsclib import TSCPrinter
from config import DEFAULT_WIDTH, DEFAULT_HEIGHT, DPI_RATIO

# 配置日志
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")


def _init_printer_settings(printer: TSCPrinter, width: str, height: str):
    """
    初始化打印机设置
    
    Args:
        printer: TSCPrinter实例
        width: 标签宽度(mm)
        height: 标签高度(mm)
    """
    # 清除缓冲区
    printer.send_command("CLS")
    
    # 设置标签尺寸（重要：先设置尺寸）
    printer.send_command(f"SIZE {width} mm, {height} mm")
    
    # 设置间隙传感器（0间隙用于连续纸或无间隙标签）
    printer.send_command("GAP 0 mm, 0 mm")
    
    # 设置打印方向（0=正常，1=镜像）
    printer.send_command("DIRECTION 0")
    
    # 设置参考点（0,0）- 从左上角开始打印
    printer.send_command("REFERENCE 0,0")
    
    # 设置偏移量为0（不偏移）
    printer.send_command("OFFSET 0 mm")
    
    # 设置打印速度（1-14，数字越小越慢但质量越好）
    printer.send_command("SPEED 4")
    
    # 设置打印浓度（0-15）
    printer.send_command("DENSITY 12")
    
    # 关闭撕离模式（避免打印撤回错位）
    # SET TEAR ON 会导致打印后回退，造成错位问题
    printer.send_command("SET TEAR OFF")
    printer.send_command("SET PEEL OFF")
    
    # 设置打印停止位置（0 = 打印后不移动纸张）
    printer.send_command("SHIFT 0")
    
    logging.info(f"打印机初始化完成: {width}mm x {height}mm")


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
        
        # 初始化打印机设置
        _init_printer_settings(p, width, height)
        
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


def print_type1(
    text_list: list[str] = None,
    width: str = None,
    height: str = None
):
    """
    Type 1: 批量纯文本打印（每张纸上下两行打印两个标签）
    
    打印方式：
    - 每张纸上下两行打印两个标签
    - 自动分组：每两个文本为一组打印在同一张纸上
    - 如果是奇数个标签，最后一张纸只打印一个
    
    固定参数：
    - width: 100mm (10cm)
    - height: 80mm (8cm)
    - 字体：宋体，56点
    
    Args:
        text_list: 要打印的文本列表，如 ["物料1", "物料2", "物料3"]
        width: 标签宽度(mm)，默认100mm（一般不需要修改）
        height: 标签高度(mm)，默认80mm（一般不需要修改）
    
    示例：
        print_type1(["物料1", "物料2", "物料3"])
        # 输出: 打印2张纸，第1张有2个标签，第2张有1个标签
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
            # 初始化打印机设置
            _init_printer_settings(p, width, height)
            
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


def print_type2(
    qr_content: str = "",
    text: str = "",
    qty: int = 1,
    width: str = None,
    height: str = None,
    qr_size: int = 8
):
    """
    Type 2: 批量二维码+文本打印（每个二维码独占一张纸）
    
    打印方式：
    - 二维码在上方，文本在下方
    - 每个二维码+文本独占一张纸
    - 适合需要单独撕下的场景
    
    固定参数：
    - width: 100mm (10cm)
    - height: 80mm (8cm)
    - qr_size: 8（二维码大小）
    - 字体：宋体，48点
    
    Args:
        qr_content: 二维码内容（URL或文本）
        text: 下方显示的文本（支持中文、英文、数字）
        qty: 打印数量（默认1张）
        width: 标签宽度(mm)，默认100mm（一般不需要修改）
        height: 标签高度(mm)，默认80mm（一般不需要修改）
        qr_size: 二维码单元宽度(1-10)，默认8（一般不需要修改）
    
    示例：
        print_type2(
            qr_content="https://example.com/product/123",
            text="产品编号-ABC123",
            qty=1
        )
        # 输出: 打印1张纸，包含二维码和文本
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
        
        # 初始化打印机设置
        _init_printer_settings(p, width, height)
        
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


def calibrate_paper():
    """
    执行纸张校准
    
    让打印机自动检测纸张位置和间隙，解决打印位置不准确的问题
    """
    p = TSCPrinter()
    try:
        logging.info("开始纸张校准...")
        p.open_port(0)
        
        # 发送自动校准命令
        p.send_command("SELFTEST")
        
        logging.info("纸张校准完成，打印机将打印测试页")
        
        p.close_port()
        return True
    except Exception as e:
        logging.error(f"纸张校准失败: {e}")
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
        
        # 初始化打印机设置
        _init_printer_settings(p, width, height)
        
        # 转换为dots（使用config中的DPI_RATIO）
        # 当前设置: {DPI_RATIO} dots/mm
        width_dots = int(float(width) * DPI_RATIO)
        height_dots = int(float(height) * DPI_RATIO)
        
        logging.info(f"打印区域: {width}mm × {height}mm = {width_dots} × {height_dots} dots (DPI比例: {DPI_RATIO})")
        
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


# ============================================================
# 兼容性别名：保留旧方法名，映射到新的 type 方法
# ============================================================

def print_batch_labels(text_list: list[str] = None, width: str = None, height: str = None):
    """兼容性别名：调用 print_type1"""
    return print_type1(text_list=text_list, width=width, height=height)


def print_qrcode_with_text(qr_content: str = "", text: str = "", qty: int = 1, 
                           width: str = None, height: str = None, qr_size: int = 8, ip: str = ""):
    """兼容性别名：调用 print_type2"""
    return print_type2(qr_content=qr_content, text=text, qty=qty, width=width, height=height, qr_size=qr_size)

