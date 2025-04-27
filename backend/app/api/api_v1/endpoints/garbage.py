from fastapi import APIRouter, UploadFile, File
from pydantic import BaseModel
from typing import List
from app.services.garbage_detection import GarbageDetectionService
from loguru import logger

class GarbageDetectionResponse(BaseModel):
    code: int = 0
    data: dict = {}
    msg: str = "success"

router = APIRouter()
detection_service = GarbageDetectionService()

@router.post("/detect", response_model=GarbageDetectionResponse)
async def detect_garbage(
    file: UploadFile = File(...)
):
    """垃圾图像识别接口"""
    try:
        # 添加日志记录上传的文件信息
        logger.info(f"开始处理图片: {file.filename}, 类型: {file.content_type}")
        
        result = await detection_service.process_image(file)
        
        # 添加日志记录处理结果
        logger.info(f"图片处理成功: {result}")
        
        return GarbageDetectionResponse(
            code=0,
            data=result,
            msg="识别成功"
        )
    except Exception as e:
        # 添加错误日志
        logger.error(f"图片处理失败: {str(e)}", exc_info=True)
        
        return GarbageDetectionResponse(
            code=1,
            data={},
            msg=f"识别失败: {str(e)}"
        )