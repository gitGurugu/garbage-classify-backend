from sqlalchemy.orm import Session
from app.models.history import SearchHistory
from typing import List
from datetime import datetime

class HistoryService:
    @staticmethod
    async def get_user_history(db: Session, user_id: int, keyword: str = None) -> List[SearchHistory]:
        """获取用户搜索历史"""
        query = db.query(SearchHistory).filter(SearchHistory.user_id == user_id)
        
        if keyword:
            query = query.filter(SearchHistory.keyword.ilike(f"%{keyword}%"))
            
        return query.order_by(SearchHistory.created_at.desc()).all()

    @staticmethod
    async def add_search_history(db: Session, user_id: int, keyword: str) -> SearchHistory:
        """添加搜索历史"""
        history = SearchHistory(
            user_id=user_id,
            keyword=keyword,
            created_at=datetime.utcnow()
        )
        db.add(history)
        db.commit()
        db.refresh(history)
        return history