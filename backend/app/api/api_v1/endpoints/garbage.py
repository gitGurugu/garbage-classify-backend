from fastapi import APIRouter, UploadFile, File, Depends
from fastapi.staticfiles import StaticFiles
from sqlalchemy.orm import Session
from app.utils import deps
from app.services.garbage_detection import GarbageDetectionService

router = APIRouter()
detection_service = GarbageDetectionService()#服务是类先实例化一个对象

@router.post("/detect")
async def detect_garbage(
    file: UploadFile = File(...),#File(...) 表示这是一个文件上传参数，并且是必填的
    #db: Session = Depends(deps.get_db)
):
    """垃圾图像识别接口"""
    result = await detection_service.process_image(file) #->str(image_url_path,audio_url_path)
    return {
        "success": True,
        "data": result 
    }
    """
    class ProcessedFilesResponse(TypedDict):
        image_url: str
        audio_url: str
        categories: List[str]
    """