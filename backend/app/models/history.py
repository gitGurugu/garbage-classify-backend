from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from app.models.base import Base
from datetime import datetime

class SearchHistory(Base):
    __tablename__ = "search_history"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    keyword = Column(String, index=True)  # 搜索关键词
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # 关联用户
    user = relationship("User", back_populates="search_histories")
    