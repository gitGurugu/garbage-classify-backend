from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.utils import deps
from app.schemas.garbage_item import SearchRequest
from app.services.garbage_search import GarbageSearchService
from app.models.user import User

router = APIRouter()

@router.post("/text",summary="搜索垃圾分类信息", tags=["garbage_item"])
async def search_garbage(
    request: SearchRequest,
    current_user: User = Depends(deps.get_current_user),
    db: Session = Depends(deps.get_db)
):
    """搜索垃圾分类信息"""
    try:
        items = await GarbageSearchService.search_items(db, request.keyword, current_user)  #GarbageItem
        return {
            "code": 0,
            "data": items,
            "msg": "查询成功"
        }
    except Exception as e:
        return {
            "code": 1,
            "data": [],
            "msg": f"查询失败: {str(e)}"
        }