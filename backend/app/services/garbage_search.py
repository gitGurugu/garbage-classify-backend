from sqlalchemy.orm import Session
from sqlalchemy import or_
from app.models.garbage_item import GarbageItem
from app.models.user import User
from app.services.history_service import HistoryService
from loguru import logger

class GarbageSearchService:
    @staticmethod
    async def search_items(db: Session, text: str, current_user: User):
        """
        搜索垃圾物品并记录搜索历史
        """
        # 添加日志：开始搜索
        logger.info(f"开始搜索，关键词: {text}, 用户ID: {current_user.id}")
        
        # 添加搜索历史
        await HistoryService.add_search_history(db, current_user.id, text)
        
        # 执行搜索
        query = db.query(GarbageItem).filter(
            or_(
                GarbageItem.objname.ilike(f"%{text}%"),
                GarbageItem.classify.ilike(f"%{text}%")
            )
        )
        
        results = query.all()
        # 添加日志：搜索结果
        logger.info(f"搜索结果数量: {len(results)}")
        for item in results:
            logger.info(f"找到物品: {item.objname}, 分类: {item.classify}")
            
        return results