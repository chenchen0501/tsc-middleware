"""
TSC打印机核心模块（跨平台）
支持USB连接（已改为使用USB模式，不再使用网络连接）
"""
import logging
from tsclib import TSCPrinter
from config import (
    DEFAULT_WIDTH, DEFAULT_HEIGHT, DPI_RATIO,
    PRINT_MARGIN,
    TYPE1_FONT_HEIGHT, TYPE1_FONT_NAME,
    TYPE2_FONT_HEIGHT, TYPE2_FONT_NAME, TYPE2_QR_SIZE, TYPE2_QR_SPACING,
    TYPE3_FONT_HEIGHT, TYPE3_FONT_NAME, TYPE3_QR_SIZE, TYPE3_QR_TEXT_SPACING
)

# 配置日志
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")


def _estimate_text_width(text: str, font_height: int) -> int:
    """
    估算文本打印宽度（单位：dots）
    
    Args:
        text: 文本内容
        font_height: 字体高度（点）
        
    Returns:
        估算的文本宽度（dots）
    """
    width = 0
    for char in text:
        # 判断是否为中文字符（包括中文标点）
        if '\u4e00' <= char <= '\u9fff' or '\u3000' <= char <= '\u303f':
            # 中文字符宽度约等于字体高度
            width += font_height
        else:
            # 英文、数字、符号宽度约为字体高度的 0.6 倍
            width += int(font_height * 0.6)
    return width


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
    
    # 设置间隙传感器（3mm间隙用于有间隙的标签纸）
    # 如果是连续纸，改为 GAP 0 mm, 0 mm
    printer.send_command("GAP 3 mm, 0 mm")
    
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
        
        # 计算打印区域尺寸（与 print_calibration_border 保持一致）
        width_dots = int(float(width) * DPI_RATIO)
        height_dots = int(float(height) * DPI_RATIO)
        
        # 有效打印区域（使用统一的边距配置）
        margin = PRINT_MARGIN
        effective_width = width_dots - 2 * margin
        effective_height = height_dots - 2 * margin
        
        # 字体大小（使用统一的配置）
        font_height = TYPE1_FONT_HEIGHT
        
        # 每两个文本为一组，打印在一张纸上（上下两行）
        for i in range(0, len(text_list), 2):
            # 初始化打印机设置
            _init_printer_settings(p, width, height)
            
            # 打印第一行（上半部分居中）
            first_text = text_list[i]
            text1_width = _estimate_text_width(first_text, font_height)
            
            # 上半部分水平垂直居中
            x1 = margin + (effective_width - text1_width) // 2
            y1 = margin + (effective_height // 2 - font_height) // 2
            
            p.print_text_windows_font(
                x=x1,
                y=y1,
                font_height=font_height,
                rotation=0,
                font_style=0,
                font_underline=0,
                font_face_name=TYPE1_FONT_NAME,
                text=first_text
            )
            
            # 打印第二行（下半部分居中，如果存在）
            if i + 1 < len(text_list):
                second_text = text_list[i + 1]
                text2_width = _estimate_text_width(second_text, font_height)
                
                # 下半部分水平垂直居中
                x2 = margin + (effective_width - text2_width) // 2
                y2 = margin + effective_height // 2 + (effective_height // 2 - font_height) // 2
                
                p.print_text_windows_font(
                    x=x2,
                    y=y2,
                    font_height=font_height,
                    rotation=0,
                    font_style=0,
                    font_underline=0,
                    font_face_name=TYPE1_FONT_NAME,
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
    qr_size: int = None
):
    """
    Type 2: 批量二维码+文本打印（每个二维码独占一张纸）
    
    打印方式：
    - 二维码在上方，文本在下方
    - 每个二维码+文本独占一张纸
    - 二维码和文本中心对齐，整体在纸张居中
    - 适合需要单独撕下的场景
    
    固定参数：
    - width: 100mm (10cm)
    - height: 80mm (8cm)
    - qr_size: 10（二维码大小，最大值）
    - 字体：宋体，48点
    
    Args:
        qr_content: 二维码内容（URL或文本）
        text: 下方显示的文本（支持中文、英文、数字）
        qty: 打印数量（默认1张）
        width: 标签宽度(mm)，默认100mm（一般不需要修改）
        height: 标签高度(mm)，默认80mm（一般不需要修改）
        qr_size: 二维码单元宽度(1-10)，默认使用配置文件中的值（一般不需要修改）
    
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
    if qr_size is None:
        qr_size = TYPE2_QR_SIZE
    
    p = TSCPrinter()
    try:
        # 打开USB端口（参数0表示第一个USB打印机）
        logging.info("使用 USB 连接打印机...")
        p.open_port(0)
        
        # 初始化打印机设置
        _init_printer_settings(p, width, height)
        
        # 计算打印区域尺寸（与 print_calibration_border 保持一致）
        width_dots = int(float(width) * DPI_RATIO)
        height_dots = int(float(height) * DPI_RATIO)
        
        # 有效打印区域（使用统一的边距配置）
        margin = PRINT_MARGIN
        effective_width = width_dots - 2 * margin
        effective_height = height_dots - 2 * margin
        
        # 字体大小（使用统一的配置）
        font_height = TYPE2_FONT_HEIGHT
        
        # 估算二维码尺寸（二维码通常是30-35个模块）
        qr_modules = 33  # 中等复杂度二维码的模块数
        qr_pixel_size = qr_size * qr_modules
        
        # 估算文本宽度
        text_width = _estimate_text_width(text, font_height)
        
        # 二维码和文本之间的间距（使用统一的配置）
        spacing = TYPE2_QR_SPACING
        
        # 计算整体高度（二维码 + 间距 + 文本）
        total_height = qr_pixel_size + spacing + font_height
        
        # 计算垂直起始位置（整体垂直居中）
        start_y = margin + (effective_height - total_height) // 2
        
        # 计算纸张中心线
        center_x = margin + effective_width // 2
        
        # 二维码水平居中（相对于纸张中心线）
        qr_x = center_x - qr_pixel_size // 2
        qr_y = start_y
        
        # 打印二维码
        p.send_command(f'QRCODE {qr_x},{qr_y},H,{qr_size},A,0,M2,"{qr_content}"')

        # 文本水平居中（相对于纸张中心线），位于二维码下方
        text_x = center_x - text_width // 2
        text_y = qr_y + qr_pixel_size + spacing
        
        # 打印文本
        p.print_text_windows_font(
            x=text_x,
            y=text_y,
            font_height=font_height,
            rotation=0,
            font_style=0,
            font_underline=0,
            font_face_name=TYPE2_FONT_NAME,
            text=text
        )
        
        # 执行打印
        p.send_command(f"PRINT {qty},1")
        
    finally:
        p.close_port()


def print_type3(
    data_list: list[str] = None,
    width: str = None,
    height: str = None
):
    """
    Type 3: 6格批量二维码+文本打印（每张纸分6个格子）
    
    打印方式：
    - 每张纸分成6个格子（3行 × 2列）
    - 每个格子左侧二维码，右侧文本
    - 二维码内容与文本内容一致
    - 自动分组：每6个数据打印一张纸
    - 如果数据不足6个，最后一张纸只打印实际数量
    
    纸张分割：
    - 原始纸张：100mm × 80mm
    - 横向2刀（3行）、纵向1刀（2列）
    - 每个格子尺寸：50mm × 26.67mm
    - 格子排列顺序：从左到右，从上到下
      (格子0) (格子1)
      (格子2) (格子3)
      (格子4) (格子5)
    
    固定参数：
    - width: 100mm (10cm)
    - height: 80mm (8cm)
    - qr_size: 5（二维码大小，适配小格子）
    - 字体：宋体，28点（适配小格子）
    
    Args:
        data_list: 要打印的数据列表，如 ["ABC123", "DEF456", ...]
                   二维码内容和显示文本均使用该值
        width: 标签宽度(mm)，默认100mm（一般不需要修改）
        height: 标签高度(mm)，默认80mm（一般不需要修改）
    
    示例：
        print_type3(["A001", "A002", "A003", "A004", "A005", "A006", "A007"])
        # 输出: 打印2张纸，第1张有6个格子，第2张有1个格子
    """
    if data_list is None:
        data_list = []
    
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
        
        # 计算打印区域尺寸
        width_dots = int(float(width) * DPI_RATIO)
        height_dots = int(float(height) * DPI_RATIO)
        
        # 有效打印区域（使用统一的边距配置）
        margin = PRINT_MARGIN
        effective_width = width_dots - 2 * margin
        effective_height = height_dots - 2 * margin
        
        # 每个格子的尺寸
        cell_width = effective_width // 2  # 2列
        cell_height = effective_height // 3  # 3行
        
        # Type 3 配置参数
        font_height = TYPE3_FONT_HEIGHT
        qr_size = TYPE3_QR_SIZE
        qr_text_spacing = TYPE3_QR_TEXT_SPACING
        
        # 估算二维码尺寸（二维码通常是30-35个模块）
        qr_modules = 33  # 中等复杂度二维码的模块数
        qr_pixel_size = qr_size * qr_modules
        
        # 每6个数据为一组，打印在一张纸上
        for page_idx in range(0, len(data_list), 6):
            # 初始化打印机设置
            _init_printer_settings(p, width, height)
            
            # 当前页的数据（最多6个）
            page_data = data_list[page_idx:page_idx + 6]
            
            # 遍历当前页的每个数据
            for cell_idx, data in enumerate(page_data):
                # 计算格子位置（从左到右，从上到下）
                col = cell_idx % 2  # 列索引：0 或 1
                row = cell_idx // 2  # 行索引：0, 1, 或 2
                
                # 格子左上角坐标
                cell_start_x = margin + col * cell_width
                cell_start_y = margin + row * cell_height
                
                # 格子内部可用区域（预留小边距）
                cell_margin = 5
                cell_content_width = cell_width - 2 * cell_margin
                cell_content_height = cell_height - 2 * cell_margin
                
                # 计算二维码和文本的水平布局
                # 二维码在左，文本在右
                
                # 估算文本宽度
                text_width = _estimate_text_width(data, font_height)
                
                # 计算总宽度（二维码 + 间距 + 文本）
                total_width = qr_pixel_size + qr_text_spacing + text_width
                
                # 计算起始X坐标（水平居中）
                if total_width <= cell_content_width:
                    start_x = cell_start_x + cell_margin + (cell_content_width - total_width) // 2
                else:
                    # 如果内容太宽，左对齐
                    start_x = cell_start_x + cell_margin
                
                # 计算二维码Y坐标（垂直居中）
                # 使用二维码和文本中较高的那个来计算垂直居中
                content_height = max(qr_pixel_size, font_height)
                start_y = cell_start_y + cell_margin + (cell_content_height - content_height) // 2
                
                # 二维码坐标
                qr_x = start_x
                qr_y = start_y
                
                # 打印二维码
                p.send_command(f'QRCODE {qr_x},{qr_y},H,{qr_size},A,0,M2,"{data}"')
                
                # 文本坐标（在二维码右侧）
                text_x = qr_x + qr_pixel_size + qr_text_spacing
                # 文本垂直居中对齐二维码
                text_y = qr_y + (qr_pixel_size - font_height) // 2
                
                # 打印文本
                p.print_text_windows_font(
                    x=text_x,
                    y=text_y,
                    font_height=font_height,
                    rotation=0,
                    font_style=0,
                    font_underline=0,
                    font_face_name=TYPE3_FONT_NAME,
                    text=data
                )
            
            # 执行打印一张
            p.send_command("PRINT 1,1")
            
    finally:
        # 确保关闭端口
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
    执行纸张校准（针对间隙标签纸）
    
    注意：适用于有间隙的标签纸
    使用 EOP 命令让打印机自动检测标签间隙
    """
    p = TSCPrinter()
    try:
        logging.info("开始纸张校准（间隙检测模式）...")
        p.open_port(0)
        
        # 重要：先设置标签尺寸和间隙类型
        # 对于有间隙的标签纸，需要设置实际的间隙值
        # 通常标签之间的间隙是 2-3mm
        p.send_command("SIZE 100 mm, 80 mm")
        p.send_command("GAP 3 mm, 0 mm")  # 间隙标签纸，设置 3mm 间隙
        
        # 使用 EOP (End of Page) 命令进行自动校准
        # 这个命令会让打印机自动检测标签间隙并调整位置
        p.send_command("EOP")
        
        # 或者使用 SELFTEST（会打印配置信息页）
        # p.send_command("SELFTEST")
        
        logging.info("纸张校准完成（间隙检测），打印机已自动调整位置")
        
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
        
        # 打印外边框（矩形）- 使用统一的边距配置
        # BOX x_start, y_start, x_end, y_end, line_thickness
        border_thickness = 3
        margin = PRINT_MARGIN
        p.send_command(f"BOX {margin},{margin},{width_dots-margin},{height_dots-margin},{border_thickness}")
        
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

