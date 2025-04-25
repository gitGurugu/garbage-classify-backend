from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from app.utils import deps
from app.services.history_service import HistoryService
from app.schemas.history import SearchHistoryResponse
from app.models.user import User
from typing import Optional

router = APIRouter()

@router.get("/search-list", response_model=SearchHistoryResponse)
async def get_search_history(
    keyword: Optional[str] = Query(None, description="搜索关键词"),
    current_user: User = Depends(deps.get_current_user),
    db: Session = Depends(deps.get_db)
):
    """获取用户搜索历史"""
    try:
        histories = await HistoryService.get_user_history(db, current_user.id, keyword)
        return SearchHistoryResponse(
            code=0,
            data=histories,
            msg="获取成功"
        )
    except Exception as e:
        return SearchHistoryResponse(
            code=1,
            data=[],
            msg=f"获取失败: {str(e)}"
        )