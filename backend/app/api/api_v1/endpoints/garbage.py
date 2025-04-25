from fastapi import APIRouter, UploadFile, File
from pydantic import BaseModel
from typing import List
from app.services.garbage_detection import GarbageDetectionService

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
        result = await detection_service.process_image(file)   #Dict
        return GarbageDetectionResponse(
            code=0,
            data=result,
            msg="识别成功"
        )
    except Exception as e:
        return GarbageDetectionResponse(
            code=1,
            data={},
            msg=f"识别失败: {str(e)}"
        )