from sqlalchemy import Column, String, ForeignKey
from sqlalchemy.orm import relationship

from app.models.base import Base

class WechatUser(Base):
    __tablename__ = "wechat_users"
    
    id = Column(String, primary_key=True, index=True)
    open_id = Column(String, unique=True, index=True, nullable=False)
    union_id = Column(String, unique=True, index=True, nullable=True)
    session_key = Column(String)
    user_id = Column(String, ForeignKey("users.id"))
    
    user = relationship("User", back_populates="wechat_user")



    