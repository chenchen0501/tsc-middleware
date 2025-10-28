"""
TSC打印服务 - FastAPI入口
提供HTTP接口控制TSC打印机（USB模式）
"""
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
from typing import Optional
from printer import print_type1, print_type2
from config import DEFAULT_WIDTH, DEFAULT_HEIGHT

app = FastAPI(
    title="TSC-Print-Service",
    version="3.0.0",
    description="零驱动USB打印中间件 | Windows部署 | USB连接模式 | 纸张: 10cm×8cm"
)

# 配置CORS中间件，支持跨域访问
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # 允许所有源访问，生产环境建议指定具体域名
    allow_credentials=True,
    allow_methods=["*"],  # 允许所有HTTP方法
    allow_headers=["*"],  # 允许所有请求头
)


class PrintItem(BaseModel):
    """
    打印项模型
    
    - type=1（纯文本）只需要 text 字段
    - type=2（二维码+文本）需要 text 和 qr_content 字段
    """
    text: str = Field(..., description="文本内容", json_schema_extra={"example": "产品名称"})
    qr_content: Optional[str] = Field(None, description="二维码内容（仅type=2需要）", json_schema_extra={"example": "https://www.example.com/product/123"})


class UnifiedPrintJob(BaseModel):
    """
    统一打印任务模型（USB模式，纸张区域10cm×8cm）
    
    支持的打印类型（type）：
    - 1: 批量纯文本打印，每张纸上下两行打印两个标签
    - 2: 批量二维码+文本打印，每个二维码独占一张纸
    
    所有打印参数（width、height、qr_size等）根据type固定，用户无需传递
    """
    type: int = Field(..., description="打印类型: 1=纯文本批量打印（每张纸两个）, 2=二维码+文本批量打印（每个独占一张）", json_schema_extra={"example": 1})
    print_list: list[PrintItem] = Field(..., description="打印项列表", json_schema_extra={"example": [{"text": "物料1"}, {"text": "物料2"}]})


@app.get("/")
def root():
    """根路径"""
    return {
        "service": "TSC-Print-Service",
        "version": "3.0.0",
        "mode": "USB",
        "docs": "/docs",
        "health": "/health"
    }


@app.get("/health")
def health():
    """健康检查"""
    return {"status": "alive", "service": "tsc-print"}


@app.post("/print")
def api_print(job: UnifiedPrintJob):
    """
    统一打印接口（USB模式）
    
    根据 type 参数选择不同的打印模式：
    
    **type = 1: 批量纯文本打印**
    - 每张纸上下两行打印两个标签
    - print_list中每个对象只需要 text 字段
    - 示例: 传入3个文本，会打印2张纸（第1张有2个标签，第2张有1个标签）
    - 固定参数: width=100mm, height=80mm
    
    **type = 2: 批量二维码+文本打印**
    - 每个二维码独占一张纸
    - print_list中每个对象需要 text 和 qr_content 字段
    - 固定参数: width=100mm, height=80mm, qr_size=8
    """
    try:
        # 验证print_list不为空
        if not job.print_list:
            raise HTTPException(
                status_code=400,
                detail="print_list参数不能为空"
            )
        
        # type = 1: 批量纯文本打印，每张纸两行
        if job.type == 1:
            # 提取文本列表
            text_list = [item.text for item in job.print_list]
            
            # 调用 Type 1 打印服务（固定参数）
            print_type1(
                text_list=text_list,
                width=DEFAULT_WIDTH,
                height=DEFAULT_HEIGHT
            )
            
            # 计算打印张数
            sheets = (len(text_list) + 1) // 2
            
            return {
                "status": "ok",
                "message": f"批量打印成功：{len(text_list)}个标签（共{sheets}张纸）"
            }
        
        # type = 2: 批量二维码+文本打印，每个独占一张纸
        elif job.type == 2:
            # 验证每个item都有qr_content
            for i, item in enumerate(job.print_list):
                if not item.qr_content:
                    raise HTTPException(
                        status_code=400,
                        detail=f"type=2时，print_list中第{i+1}个对象的qr_content不能为空"
                    )
            
            # 批量打印二维码（每个独占一张）
            for item in job.print_list:
                print_type2(
                    qr_content=item.qr_content,
                    text=item.text,
                    qty=1,  # 固定每次打印1张
                    width=DEFAULT_WIDTH,  # 固定100mm
                    height=DEFAULT_HEIGHT,  # 固定80mm
                    qr_size=8  # 固定二维码大小为8
                )
            
            return {
                "status": "ok",
                "message": f"二维码批量打印成功：{len(job.print_list)}张标签"
            }
        
        # 不支持的type
        else:
            raise HTTPException(
                status_code=400,
                detail=f"不支持的打印类型: type={job.type}，目前仅支持 1（纯文本批量） 和 2（二维码批量）"
            )
    
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"打印失败: {str(e)}"
        )


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)

