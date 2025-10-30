"""
TSC打印服务 - FastAPI入口
提供HTTP接口控制TSC打印机（USB模式）
使用模板系统支持多种打印场景
"""
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
from typing import Optional, Literal, List, Union
from printer import (
    print_type1, print_type2, test_connection,
    _init_printer_settings, _estimate_text_width
)
from tsclib import TSCPrinter
from config import (
    DEFAULT_WIDTH, DEFAULT_HEIGHT, DPI_RATIO, PRINT_MARGIN,
    TYPE1_FONT_HEIGHT, TYPE1_FONT_NAME,
    TYPE2_FONT_HEIGHT, TYPE2_FONT_NAME, TYPE2_QR_SIZE, TYPE2_QR_SPACING
)
import logging

# 配置日志
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

app = FastAPI(
    title="TSC-Print-Middleware",
    version="3.0.0",
    description="TSC打印机USB中间件 | 模板化打印 | Windows部署 | 纸张: 10cm×8cm"
)

# 配置CORS中间件，支持跨域访问
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # 允许所有源访问，生产环境建议指定具体域名
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# ============================================================
# 数据模型定义
# ============================================================

class TextElement(BaseModel):
    """文本元素"""
    type: Literal["text"] = "text"
    x: int = Field(..., description="X坐标 (dots)", ge=0)
    y: int = Field(..., description="Y坐标 (dots)", ge=0)
    text: str = Field(..., description="文本内容")
    font_size: int = Field(48, description="字体大小 (dots)", ge=12, le=120)
    font_name: str = Field("宋体", description="字体名称")


class QRCodeElement(BaseModel):
    """二维码元素"""
    type: Literal["qrcode"] = "qrcode"
    x: int = Field(..., description="X坐标 (dots)", ge=0)
    y: int = Field(..., description="Y坐标 (dots)", ge=0)
    content: str = Field(..., description="二维码内容")
    size: int = Field(10, description="二维码单元宽度 (1-10)", ge=1, le=10)


class BarcodeElement(BaseModel):
    """条形码元素"""
    type: Literal["barcode"] = "barcode"
    x: int = Field(..., description="X坐标 (dots)", ge=0)
    y: int = Field(..., description="Y坐标 (dots)", ge=0)
    content: str = Field(..., description="条形码内容")
    height: int = Field(80, description="条形码高度 (dots)", ge=30, le=300)
    barcode_type: str = Field("128", description="条形码类型 (128, EAN13等)")


class CustomLayout(BaseModel):
    """自定义布局"""
    width: Optional[int] = Field(None, description="标签宽度(mm)")
    height: Optional[int] = Field(None, description="标签高度(mm)")
    elements: List[Union[TextElement, QRCodeElement, BarcodeElement]] = Field(
        ..., 
        description="打印元素列表",
        discriminator="type"
    )


class SingleTextData(BaseModel):
    """单行文本数据"""
    text: str = Field(..., description="文本内容")


class DoubleTextData(BaseModel):
    """双行文本数据"""
    text1: str = Field(..., description="第一行文本")
    text2: str = Field(..., description="第二行文本")


class QRCodeWithTextData(BaseModel):
    """二维码+文本数据"""
    qrcode: str = Field(..., description="二维码内容")
    text: str = Field(..., description="文本内容")


class BarcodeWithTextData(BaseModel):
    """条形码+文本数据"""
    barcode: str = Field(..., description="条形码内容")
    text: str = Field(..., description="文本内容")


class PrintJob(BaseModel):
    """打印任务模型"""
    template: Literal["single-text", "double-text", "qrcode-with-text", "barcode-with-text", "custom"] = Field(
        ..., 
        description="模板名称"
    )
    print_list: Optional[List[Union[SingleTextData, DoubleTextData, QRCodeWithTextData, BarcodeWithTextData]]] = Field(
        None,
        description="批量打印数据列表（预设模板使用）"
    )
    layout: Optional[CustomLayout] = Field(
        None,
        description="自定义布局（仅template=custom时使用）"
    )
    qty: int = Field(1, description="打印数量（仅custom模板使用）", ge=1, le=100)


# ============================================================
# API 路由
# ============================================================

@app.get("/")
def root():
    """根路径"""
    return {
        "service": "TSC-Print-Middleware",
        "version": "3.0.0",
        "mode": "USB",
        "docs": "/docs",
        "health": "/health",
        "templates": ["single-text", "double-text", "qrcode-with-text", "barcode-with-text", "custom"]
    }


@app.get("/health")
def health():
    """健康检查"""
    return {"status": "alive", "service": "tsc-print-middleware"}


@app.post("/test")
def api_test():
    """
    测试USB打印机连接
    
    返回打印机连接状态
    """
    try:
        if test_connection():
            return {
                "status": "ok",
                "message": "USB打印机连接成功"
            }
        else:
            raise HTTPException(
                status_code=503,
                detail="USB打印机连接失败"
            )
    except Exception as e:
        raise HTTPException(
            status_code=503,
            detail=f"USB打印机连接失败: {str(e)}"
        )


@app.post("/print")
def api_print(job: PrintJob):
    """
    统一打印接口（模板系统）
    
    支持的模板：
    
    **1. single-text - 单行文本居中**
    - print_list: [{"text": "文本"}]
    
    **2. double-text - 双行文本（上下居中）**
    - print_list: [{"text1": "第一行", "text2": "第二行"}]
    - 注意：会将连续两条数据打印在同一张纸上
    
    **3. qrcode-with-text - 二维码+文本**
    - print_list: [{"qrcode": "url", "text": "文本"}]
    
    **4. barcode-with-text - 条形码+文本**
    - print_list: [{"barcode": "123456", "text": "文本"}]
    
    **5. custom - 完全自定义布局**
    - layout: {width, height, elements: [...]}
    - qty: 打印数量
    """
    try:
        # ========== 预设模板处理 ==========
        if job.template == "single-text":
            return handle_single_text(job)
        
        elif job.template == "double-text":
            return handle_double_text(job)
        
        elif job.template == "qrcode-with-text":
            return handle_qrcode_with_text(job)
        
        elif job.template == "barcode-with-text":
            return handle_barcode_with_text(job)
        
        # ========== 自定义布局 ==========
        elif job.template == "custom":
            return handle_custom_layout(job)
        
        else:
            raise HTTPException(
                status_code=400,
                detail=f"不支持的模板类型: {job.template}"
            )
    
    except HTTPException:
        raise
    except Exception as e:
        logging.error(f"打印失败: {e}")
        raise HTTPException(
            status_code=500,
            detail=f"打印失败: {str(e)}"
        )


# ============================================================
# 模板处理函数
# ============================================================

def handle_single_text(job: PrintJob):
    """处理单行文本模板"""
    if not job.print_list:
        raise HTTPException(status_code=400, detail="print_list不能为空")
    
    p = TSCPrinter()
    try:
        p.open_port(0)
        
        width_dots = int(float(DEFAULT_WIDTH) * DPI_RATIO)
        height_dots = int(float(DEFAULT_HEIGHT) * DPI_RATIO)
        effective_width = width_dots - 2 * PRINT_MARGIN
        effective_height = height_dots - 2 * PRINT_MARGIN
        
        for item in job.print_list:
            _init_printer_settings(p, DEFAULT_WIDTH, DEFAULT_HEIGHT)
            
            text = item.text
            font_height = TYPE1_FONT_HEIGHT
            text_width = _estimate_text_width(text, font_height)
            
            # 水平垂直居中
            x = PRINT_MARGIN + (effective_width - text_width) // 2
            y = PRINT_MARGIN + (effective_height - font_height) // 2
            
            p.print_text_windows_font(
                x=x, y=y,
                font_height=font_height,
                rotation=0,
                font_style=0,
                font_underline=0,
                font_face_name=TYPE1_FONT_NAME,
                text=text
            )
            
            p.send_command("PRINT 1,1")
        
        return {
            "status": "ok",
            "message": f"单行文本打印成功：{len(job.print_list)}张标签"
        }
    finally:
        p.close_port()


def handle_double_text(job: PrintJob):
    """处理双行文本模板（每张纸两个标签）"""
    if not job.print_list:
        raise HTTPException(status_code=400, detail="print_list不能为空")
    
    p = TSCPrinter()
    try:
        p.open_port(0)
        
        width_dots = int(float(DEFAULT_WIDTH) * DPI_RATIO)
        height_dots = int(float(DEFAULT_HEIGHT) * DPI_RATIO)
        effective_width = width_dots - 2 * PRINT_MARGIN
        effective_height = height_dots - 2 * PRINT_MARGIN
        font_height = TYPE1_FONT_HEIGHT
        
        # 每两个为一组，打印在同一张纸上
        for i in range(0, len(job.print_list), 2):
            _init_printer_settings(p, DEFAULT_WIDTH, DEFAULT_HEIGHT)
            
            # 第一行（上半部分）
            item1 = job.print_list[i]
            text1 = item1.text1 if hasattr(item1, 'text1') else item1.text
            text1_width = _estimate_text_width(text1, font_height)
            
            x1 = PRINT_MARGIN + (effective_width - text1_width) // 2
            y1 = PRINT_MARGIN + (effective_height // 2 - font_height) // 2
            
            p.print_text_windows_font(
                x=x1, y=y1,
                font_height=font_height,
                rotation=0,
                font_style=0,
                font_underline=0,
                font_face_name=TYPE1_FONT_NAME,
                text=text1
            )
            
            # 第二行（下半部分，如果存在）
            if i + 1 < len(job.print_list):
                item2 = job.print_list[i + 1]
                text2 = item2.text2 if hasattr(item2, 'text2') else item2.text if hasattr(item2, 'text') else item2.text1
                text2_width = _estimate_text_width(text2, font_height)
                
                x2 = PRINT_MARGIN + (effective_width - text2_width) // 2
                y2 = PRINT_MARGIN + effective_height // 2 + (effective_height // 2 - font_height) // 2
                
                p.print_text_windows_font(
                    x=x2, y=y2,
                    font_height=font_height,
                    rotation=0,
                    font_style=0,
                    font_underline=0,
                    font_face_name=TYPE1_FONT_NAME,
                    text=text2
                )
            
            p.send_command("PRINT 1,1")
        
        sheets = (len(job.print_list) + 1) // 2
        return {
            "status": "ok",
            "message": f"双行文本打印成功：{len(job.print_list)}个标签（共{sheets}张纸）"
        }
    finally:
        p.close_port()


def handle_qrcode_with_text(job: PrintJob):
    """处理二维码+文本模板"""
    if not job.print_list:
        raise HTTPException(status_code=400, detail="print_list不能为空")
    
    for item in job.print_list:
        print_type2(
            qr_content=item.qrcode,
            text=item.text,
            qty=1,
            width=DEFAULT_WIDTH,
            height=DEFAULT_HEIGHT,
            qr_size=TYPE2_QR_SIZE
        )
    
    return {
        "status": "ok",
        "message": f"二维码标签打印成功：{len(job.print_list)}张"
    }


def handle_barcode_with_text(job: PrintJob):
    """处理条形码+文本模板"""
    if not job.print_list:
        raise HTTPException(status_code=400, detail="print_list不能为空")
    
    p = TSCPrinter()
    try:
        p.open_port(0)
        
        width_dots = int(float(DEFAULT_WIDTH) * DPI_RATIO)
        height_dots = int(float(DEFAULT_HEIGHT) * DPI_RATIO)
        effective_width = width_dots - 2 * PRINT_MARGIN
        effective_height = height_dots - 2 * PRINT_MARGIN
        
        for item in job.print_list:
            _init_printer_settings(p, DEFAULT_WIDTH, DEFAULT_HEIGHT)
            
            barcode_height = 80
            font_height = TYPE2_FONT_HEIGHT
            spacing = TYPE2_QR_SPACING
            
            # 估算条形码宽度（Code 128大约每个字符10 dots）
            barcode_width = len(item.barcode) * 10 + 40
            text_width = _estimate_text_width(item.text, font_height)
            
            total_height = barcode_height + spacing + font_height
            start_y = PRINT_MARGIN + (effective_height - total_height) // 2
            center_x = PRINT_MARGIN + effective_width // 2
            
            # 条形码居中
            barcode_x = center_x - barcode_width // 2
            barcode_y = start_y
            
            p.send_command(f'BARCODE {barcode_x},{barcode_y},"128",{barcode_height},1,0,2,2,"{item.barcode}"')
            
            # 文本居中
            text_x = center_x - text_width // 2
            text_y = barcode_y + barcode_height + spacing
            
            p.print_text_windows_font(
                x=text_x, y=text_y,
                font_height=font_height,
                rotation=0,
                font_style=0,
                font_underline=0,
                font_face_name=TYPE2_FONT_NAME,
                text=item.text
            )
            
            p.send_command("PRINT 1,1")
        
        return {
            "status": "ok",
            "message": f"条形码标签打印成功：{len(job.print_list)}张"
        }
    finally:
        p.close_port()


def handle_custom_layout(job: PrintJob):
    """处理自定义布局"""
    if not job.layout:
        raise HTTPException(status_code=400, detail="custom模板需要提供layout参数")
    
    if not job.layout.elements:
        raise HTTPException(status_code=400, detail="layout.elements不能为空")
    
    width = str(job.layout.width) if job.layout.width else DEFAULT_WIDTH
    height = str(job.layout.height) if job.layout.height else DEFAULT_HEIGHT
    
    p = TSCPrinter()
    try:
        p.open_port(0)
        _init_printer_settings(p, width, height)
        
        # 渲染所有元素
        for element in job.layout.elements:
            if element.type == "text":
                p.print_text_windows_font(
                    x=element.x,
                    y=element.y,
                    font_height=element.font_size,
                    rotation=0,
                    font_style=0,
                    font_underline=0,
                    font_face_name=element.font_name,
                    text=element.text
                )
            
            elif element.type == "qrcode":
                p.send_command(f'QRCODE {element.x},{element.y},H,{element.size},A,0,M2,"{element.content}"')
            
            elif element.type == "barcode":
                p.send_command(f'BARCODE {element.x},{element.y},"{element.barcode_type}",{element.height},1,0,2,2,"{element.content}"')
        
        # 打印
        p.send_command(f"PRINT {job.qty},1")
        
        return {
            "status": "ok",
            "message": f"自定义布局打印成功：{job.qty}张"
        }
    finally:
        p.close_port()


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
