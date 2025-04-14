from sqlalchemy import Column, Integer, String, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from datetime import datetime
from app.models import Base

class WechatUser(Base):
    __tablename__ = "wechat_users"

    id = Column(Integer, primary_key=True, index=True)
    open_id = Column(String(50), unique=True, index=True, nullable=False)
    union_id = Column(String(50), index=True)
    session_key = Column(String(50))
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # 建立与 User 模型的关系
    user = relationship("User", backref="wechat_user")



# 关注点分离
# User 表关注用户的基本信息
# WechatUser 表关注微信平台相关的信息