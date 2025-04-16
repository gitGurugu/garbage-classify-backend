from datetime import datetime
from sqlalchemy import Column, Integer, String, DateTime
from app.models import Base

class User(Base):
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True, index=True)
    nickname = Column(String, index=True)
    avatar_url = Column(String)  # 添加头像URL字段
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)