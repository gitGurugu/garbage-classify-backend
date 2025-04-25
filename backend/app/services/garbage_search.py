from sqlalchemy.orm import Session
from sqlalchemy import or_
from app.models.garbage_item import GarbageItem
from app.models.user import User
from app.services.history_service import HistoryService

class GarbageSearchService:
    @staticmethod
    async def search_items(db: Session, keyword: str, current_user: User):
        """
        搜索垃圾物品并记录搜索历史
        """
        # 添加搜索历史
        await HistoryService.add_search_history(db, current_user.id, keyword)
        
        # 执行搜索
        query = db.query(GarbageItem).filter(
            or_(
                GarbageItem.objname.ilike(f"%{keyword}%"),
                GarbageItem.classify.ilike(f"%{keyword}%")
            )
        )
        return query.all()