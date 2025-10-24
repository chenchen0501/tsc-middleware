"""
TSC打印服务 - FastAPI入口
提供HTTP接口控制TSC打印机
"""
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field
from printer import print_label, print_qrcode, test_connection, print_batch_labels
from config import PRINTER_IP

app = FastAPI(
    title="TSC-Print-Service",
    version="1.0.0",
    description="零驱动局域网打印中间件 | macOS开发 ➜ Windows部署"
)


class PrintJob(BaseModel):
    """打印任务模型"""
    ip: str | None = Field(None, description="打印机IP地址（可选，默认使用配置的IP）", json_schema_extra={"example": "192.168.1.100"})
    text: str = Field(..., description="标签文本", json_schema_extra={"example": "Hello M4"})
    barcode: str = Field("", description="条形码内容（可选）", json_schema_extra={"example": "1234567890"})
    qty: int = Field(1, ge=1, le=100, description="打印数量")
    width: str = Field("100", description="标签宽度(mm)")
    height: str = Field("90", description="标签高度(mm)")


class QRCodeJob(BaseModel):
    """二维码打印任务模型"""
    ip: str | None = Field(None, description="打印机IP地址（可选，默认使用配置的IP）", json_schema_extra={"example": "192.168.1.100"})
    content: str = Field(..., description="二维码内容", json_schema_extra={"example": "https://www.example.com"})
    text: str = Field("", description="标签文本（可选）")
    qty: int = Field(1, ge=1, le=100, description="打印数量")
    width: str = Field("100", description="标签宽度(mm)")
    height: str = Field("90", description="标签高度(mm)")
    qr_size: int = Field(8, ge=1, le=10, description="二维码大小(1-10)")


class BatchPrintJob(BaseModel):
    """批量打印任务模型"""
    ip: str | None = Field(None, description="打印机IP地址（可选，默认使用配置的IP）", json_schema_extra={"example": "192.168.1.100"})
    text_list: list[str] = Field(
        ..., 
        description="要打印的文本列表", 
        json_schema_extra={"example": ["cc测试拆箱物料1_盖子_1_1", "cc测试拆箱物料2_底座_1_2", "cc测试拆箱物料3_配件_1_3"]}
    )
    width: str = Field("100", description="标签宽度(mm)")
    height: str = Field("90", description="标签高度(mm)")


class TestConnectionRequest(BaseModel):
    """测试连接请求"""
    ip: str | None = Field(None, description="打印机IP地址（可选，默认使用配置的IP）", json_schema_extra={"example": "192.168.1.100"})


@app.get("/")
def root():
    """根路径"""
    return {
        "service": "TSC-Print-Service",
        "version": "1.0.0",
        "docs": "/docs",
        "health": "/health"
    }


@app.get("/health")
def health():
    """健康检查"""
    return {"status": "alive", "service": "tsc-print"}


@app.post("/print")
def api_print(job: PrintJob):
    """
    打印标签
    
    - **ip**: 打印机IP地址（可选，默认使用配置的IP）
    - **text**: 标签上的文本内容
    - **barcode**: 条形码数据（可选）
    - **qty**: 打印数量（1-100）
    - **width**: 标签宽度，单位mm（默认100）
    - **height**: 标签高度，单位mm（默认90）
    """
    try:
        printer_ip = job.ip or PRINTER_IP
        print_label(
            ip=printer_ip,
            text=job.text,
            barcode=job.barcode,
            qty=job.qty,
            width=job.width,
            height=job.height
        )
        return {
            "status": "ok",
            "message": f"成功发送{job.qty}张标签到打印机 {printer_ip}"
        }
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"打印失败: {str(e)}"
        )


@app.post("/print/qrcode")
def api_print_qrcode(job: QRCodeJob):
    """
    打印二维码标签
    
    - **ip**: 打印机IP地址（可选，默认使用配置的IP）
    - **content**: 二维码内容（URL或文本）
    - **text**: 标签文本（可选）
    - **qty**: 打印数量（1-100）
    - **width**: 标签宽度，单位mm（默认100）
    - **height**: 标签高度，单位mm（默认90）
    - **qr_size**: 二维码大小（1-10，默认8）
    """
    try:
        printer_ip = job.ip or PRINTER_IP
        print_qrcode(
            ip=printer_ip,
            content=job.content,
            text=job.text,
            qty=job.qty,
            width=job.width,
            height=job.height,
            qr_size=job.qr_size
        )
        return {
            "status": "ok",
            "message": f"成功发送{job.qty}张二维码标签到打印机 {printer_ip}"
        }
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"打印失败: {str(e)}"
        )


@app.post("/print/batch")
def api_print_batch(job: BatchPrintJob):
    """
    批量打印标签（每张纸上下两行打印两个标签）
    
    - **ip**: 打印机IP地址（可选，默认使用配置的IP）
    - **text_list**: 要打印的文本列表，每两个文本打印在一张纸的上下两行
    - **width**: 标签宽度，单位mm（默认100）
    - **height**: 标签高度，单位mm（默认90）
    
    示例：传入3个文本，会打印2张纸（第1张有2个标签，第2张有1个标签）
    """
    try:
        if not job.text_list:
            raise HTTPException(
                status_code=400,
                detail="文本列表不能为空"
            )
        
        printer_ip = job.ip or PRINTER_IP
        print_batch_labels(
            ip=printer_ip,
            text_list=job.text_list,
            width=job.width,
            height=job.height
        )
        
        # 计算打印张数
        sheets = (len(job.text_list) + 1) // 2
        
        return {
            "status": "ok",
            "message": f"成功发送{len(job.text_list)}个标签（共{sheets}张纸）到打印机 {printer_ip}"
        }
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"批量打印失败: {str(e)}"
        )


@app.post("/test")
def api_test_connection(req: TestConnectionRequest):
    """
    测试打印机连接
    
    - **ip**: 打印机IP地址（可选，默认使用配置的IP）
    """
    try:
        printer_ip = req.ip or PRINTER_IP
        is_connected = test_connection(printer_ip)
        if is_connected:
            return {
                "status": "ok",
                "message": f"打印机 {printer_ip} 连接正常"
            }
        else:
            raise HTTPException(
                status_code=503,
                detail=f"无法连接到打印机 {printer_ip}"
            )
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"连接测试失败: {str(e)}"
        )


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)

