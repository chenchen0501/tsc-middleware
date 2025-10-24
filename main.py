"""
TSC打印服务 - FastAPI入口
提供HTTP接口控制TSC打印机
"""
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field
from printer import print_label, print_qrcode, test_connection

app = FastAPI(
    title="TSC-Print-Service",
    version="1.0.0",
    description="零驱动局域网打印中间件 | macOS开发 ➜ Windows部署"
)


class PrintJob(BaseModel):
    """打印任务模型"""
    ip: str = Field(..., description="打印机IP地址", json_schema_extra={"example": "192.168.1.100"})
    text: str = Field(..., description="标签文本", json_schema_extra={"example": "Hello M4"})
    barcode: str = Field(..., description="条形码内容", json_schema_extra={"example": "1234567890"})
    qty: int = Field(1, ge=1, le=100, description="打印数量")
    width: str = Field("100", description="标签宽度(mm)")
    height: str = Field("90", description="标签高度(mm)")


class QRCodeJob(BaseModel):
    """二维码打印任务模型"""
    ip: str = Field(..., description="打印机IP地址", json_schema_extra={"example": "192.168.1.100"})
    content: str = Field(..., description="二维码内容", json_schema_extra={"example": "https://www.example.com"})
    text: str = Field("", description="标签文本（可选）")
    qty: int = Field(1, ge=1, le=100, description="打印数量")
    width: str = Field("100", description="标签宽度(mm)")
    height: str = Field("90", description="标签高度(mm)")
    qr_size: int = Field(8, ge=1, le=10, description="二维码大小(1-10)")


class TestConnectionRequest(BaseModel):
    """测试连接请求"""
    ip: str = Field(..., description="打印机IP地址", json_schema_extra={"example": "192.168.1.100"})


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
    
    - **ip**: 打印机IP地址
    - **text**: 标签上的文本内容
    - **barcode**: 条形码数据
    - **qty**: 打印数量（1-100）
    - **width**: 标签宽度，单位mm（默认100）
    - **height**: 标签高度，单位mm（默认90）
    """
    try:
        print_label(
            ip=job.ip,
            text=job.text,
            barcode=job.barcode,
            qty=job.qty,
            width=job.width,
            height=job.height
        )
        return {
            "status": "ok",
            "message": f"成功发送{job.qty}张标签到打印机 {job.ip}"
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
    
    - **ip**: 打印机IP地址
    - **content**: 二维码内容（URL或文本）
    - **text**: 标签文本（可选）
    - **qty**: 打印数量（1-100）
    - **width**: 标签宽度，单位mm（默认100）
    - **height**: 标签高度，单位mm（默认90）
    - **qr_size**: 二维码大小（1-10，默认8）
    """
    try:
        print_qrcode(
            ip=job.ip,
            content=job.content,
            text=job.text,
            qty=job.qty,
            width=job.width,
            height=job.height,
            qr_size=job.qr_size
        )
        return {
            "status": "ok",
            "message": f"成功发送{job.qty}张二维码标签到打印机 {job.ip}"
        }
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"打印失败: {str(e)}"
        )


@app.post("/test")
def api_test_connection(req: TestConnectionRequest):
    """
    测试打印机连接
    
    - **ip**: 打印机IP地址
    """
    try:
        is_connected = test_connection(req.ip)
        if is_connected:
            return {
                "status": "ok",
                "message": f"打印机 {req.ip} 连接正常"
            }
        else:
            raise HTTPException(
                status_code=503,
                detail=f"无法连接到打印机 {req.ip}"
            )
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"连接测试失败: {str(e)}"
        )


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)

