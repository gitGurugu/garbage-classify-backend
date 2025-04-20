from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from typing import List
from app.utils import deps
from app.schemas.garbage import GarbageSearchResponse
from app.services.garbage_search import GarbageSearchService

router = APIRouter()

@router.get("/search-list", response_model=GarbageSearchResponse)
async def search_garbage(
    keyword: str = Query(..., description="搜索关键词"),
    db: Session = Depends(deps.get_db)
):
    """搜索垃圾分类信息"""
    try:
        items = await GarbageSearchService.search_items(db, keyword)
        return GarbageSearchResponse(
            code=0,
            data=items,
            msg="查询成功"
        )
    except Exception as e:
        return GarbageSearchResponse(
            code=1,
            data=[],
            msg=f"查询失败: {str(e)}"
        )