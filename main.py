"""
TSC打印服务 - FastAPI入口
提供HTTP接口控制TSC打印机（USB模式）
"""
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field
from printer import print_label, print_qrcode, test_connection, print_batch_labels
from config import DEFAULT_WIDTH, DEFAULT_HEIGHT

app = FastAPI(
    title="TSC-Print-Service",
    version="2.0.0",
    description="零驱动USB打印中间件 | macOS开发 ➜ Windows部署 | USB连接模式 | 纸张: 10cm×8cm"
)


class PrintJob(BaseModel):
    """打印任务模型（USB模式，纸张区域10cm×8cm）"""
    text: str = Field(..., description="标签文本", json_schema_extra={"example": "Hello TSC USB"})
    barcode: str = Field("", description="条形码内容（可选）", json_schema_extra={"example": "1234567890"})
    qty: int = Field(1, ge=1, le=100, description="打印数量")
    width: str = Field(DEFAULT_WIDTH, description="标签宽度(mm)", json_schema_extra={"example": "100"})
    height: str = Field(DEFAULT_HEIGHT, description="标签高度(mm)", json_schema_extra={"example": "80"})


class QRCodeJob(BaseModel):
    """二维码打印任务模型（USB模式，纸张区域10cm×8cm）"""
    content: str = Field(..., description="二维码内容", json_schema_extra={"example": "https://www.example.com"})
    text: str = Field("", description="标签文本（可选）")
    qty: int = Field(1, ge=1, le=100, description="打印数量")
    width: str = Field(DEFAULT_WIDTH, description="标签宽度(mm)", json_schema_extra={"example": "100"})
    height: str = Field(DEFAULT_HEIGHT, description="标签高度(mm)", json_schema_extra={"example": "80"})
    qr_size: int = Field(8, ge=1, le=10, description="二维码大小(1-10)")


class BatchPrintJob(BaseModel):
    """批量打印任务模型（USB模式，纸张区域10cm×8cm）"""
    text_list: list[str] = Field(
        ..., 
        description="要打印的文本列表", 
        json_schema_extra={"example": ["cc测试拆箱物料1_盖子_1_1", "cc测试拆箱物料2_底座_1_2", "cc测试拆箱物料3_配件_1_3"]}
    )
    width: str = Field(DEFAULT_WIDTH, description="标签宽度(mm)", json_schema_extra={"example": "100"})
    height: str = Field(DEFAULT_HEIGHT, description="标签高度(mm)", json_schema_extra={"example": "80"})


@app.get("/")
def root():
    """根路径"""
    return {
        "service": "TSC-Print-Service",
        "version": "2.0.0",
        "mode": "USB",
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
    打印标签（USB模式）
    
    - **text**: 标签上的文本内容
    - **barcode**: 条形码数据（可选）
    - **qty**: 打印数量（1-100）
    - **width**: 标签宽度，单位mm（默认100）
    - **height**: 标签高度，单位mm（默认90）
    """
    try:
        print_label(
            text=job.text,
            barcode=job.barcode,
            qty=job.qty,
            width=job.width,
            height=job.height
        )
        return {
            "status": "ok",
            "message": f"成功发送{job.qty}张标签到USB打印机"
        }
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"打印失败: {str(e)}"
        )


@app.post("/print/qrcode")
def api_print_qrcode(job: QRCodeJob):
    """
    打印二维码标签（USB模式）
    
    - **content**: 二维码内容（URL或文本）
    - **text**: 标签文本（可选）
    - **qty**: 打印数量（1-100）
    - **width**: 标签宽度，单位mm（默认100）
    - **height**: 标签高度，单位mm（默认90）
    - **qr_size**: 二维码大小（1-10，默认8）
    """
    try:
        print_qrcode(
            content=job.content,
            text=job.text,
            qty=job.qty,
            width=job.width,
            height=job.height,
            qr_size=job.qr_size
        )
        return {
            "status": "ok",
            "message": f"成功发送{job.qty}张二维码标签到USB打印机"
        }
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"打印失败: {str(e)}"
        )


@app.post("/print/batch")
def api_print_batch(job: BatchPrintJob):
    """
    批量打印标签（USB模式，每张纸上下两行打印两个标签）
    
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
        
        print_batch_labels(
            text_list=job.text_list,
            width=job.width,
            height=job.height
        )
        
        # 计算打印张数
        sheets = (len(job.text_list) + 1) // 2
        
        return {
            "status": "ok",
            "message": f"成功发送{len(job.text_list)}个标签（共{sheets}张纸）到USB打印机"
        }
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"批量打印失败: {str(e)}"
        )


@app.post("/test")
def api_test_connection():
    """
    测试USB打印机连接
    """
    try:
        is_connected = test_connection()
        if is_connected:
            return {
                "status": "ok",
                "message": "USB打印机连接正常"
            }
        else:
            raise HTTPException(
                status_code=503,
                detail="无法连接到USB打印机"
            )
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"连接测试失败: {str(e)}"
        )


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)

