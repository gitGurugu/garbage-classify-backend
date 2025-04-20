from sqlalchemy import Column, Integer, String
from app.models.base import Base

class GarbageItem(Base):
    __tablename__ = "garbage_items"

    id = Column(Integer, primary_key=True, index=True)
    objname = Column(String, index=True)  # 物品名称
    classify = Column(String)  # 垃圾分类
    attention = Column(String)  # 注意事项