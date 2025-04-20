from sqlalchemy.orm import Session
from sqlalchemy import or_
from app.models.garbage_item import GarbageItem

class GarbageSearchService:
    @staticmethod
    async def search_items(db: Session, keyword: str):
        """
        搜索垃圾物品
        """
        query = db.query(GarbageItem).filter(
            or_(
                GarbageItem.objname.ilike(f"%{keyword}%"),
                GarbageItem.classify.ilike(f"%{keyword}%")
            )
        )
        return query.all()