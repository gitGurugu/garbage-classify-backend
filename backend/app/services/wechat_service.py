import requests
from fastapi import HTTPException
from sqlalchemy.orm import Session

from app.core.config import settings
from app.models.user import User
from app.models.wechat_user import WechatUser
from app.core.security import create_access_token
from datetime import datetime

class WeChatService:
    @staticmethod
    async def login_with_code(db: Session, code: str):
        # 微信登录凭证校验接口地址
        url = "https://api.weixin.qq.com/sns/jscode2session"
        params = {
            "appid": settings.WECHAT_APP_ID,
            "secret": settings.WECHAT_APP_SECRET,
            "js_code": code,
            "grant_type": "authorization_code"
        }
        
        response = requests.get(url, params=params)
        result = response.json()
        
        if "errcode" in result:
            raise HTTPException(status_code=400, detail="微信登录失败")
            
        open_id = result.get("openid")
        # get 方法的主要作用是从字典中安全地获取一个键的值，如果该键不存在，可以返回一个默认值，而不是抛出 KeyError 异常。
        session_key = result.get("session_key")
        union_id = result.get("unionid")
        
        # 查找或创建微信用户
        wechat_user = db.query(WechatUser).filter(WechatUser.open_id == open_id).first()
        
        if not wechat_user:
            # 创建新用户
            now=datetime.utcnow()
            user = User(
                nickname=f"用户{open_id[:8]}", # 可以根据需求设置默认昵称
                created_at=now,
                updated_at=now
            )
            db.add(user)
            db.flush()
            
            wechat_user = WechatUser(
                open_id=open_id,
                union_id=union_id,
                session_key=session_key,
                user_id=user.id,
                created_at=now,
                updated_at=now
            )
            db.add(wechat_user)
            db.commit()
        else:
            # 更新session_key
            wechat_user.session_key = session_key
            wechat_user.updated_at = datetime.utcnow()
            db.commit()

        # 生成访问令牌
        access_token = create_access_token(wechat_user.user_id)
        
        return {
            "access_token": access_token,
            "token_type": "bearer",
            "user_id": wechat_user.user_id
        }