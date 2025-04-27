import requests
from fastapi import HTTPException #异常类
from sqlalchemy.orm import Session

from app.core.config import settings
from app.models.user import User
from app.models.wechat_user import WechatUser
from app.core.security import create_access_token
from datetime import datetime

class WeChatService:
    @staticmethod #表示这是一个静态方法，不需要实例化类即可调用。
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
        result = response.json() #将响应的 JSON 数据解析为 Python 字典对象
        #使用 requests 库发起一个 HTTP 请求并得到一个响应（response）时，可以使用 .json() 方法来解析响应体中的 JSON 数据

        
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
            #添加对象到会话：将一个或多个对象添加到当前会话中，但不会立即保存到数据库中。准备插入操作：这些对象在调用 db.commit() 之前不会被保存到数据库中。
            db.flush()
            
            wechat_user = WechatUser(
                open_id=open_id,#open_id 是用户在当前小程序或公众号下的唯一标识符，是微信用户的唯一标识
                union_id=union_id,#union_id 是用户在同一开放平台下的唯一标识符，用于关联不同应用、公众号和小程序中的用户，在用户将多个微信账号（如公众号、小程序等）关联到同一开放平台账号时，可以获取到 union_id
                session_key=session_key,
                user_id=user.id,#数据库自动生成id，外键，使微信用户wechatuser和user关联
                created_at=now,
                updated_at=now
            )
            db.add(wechat_user)
            db.commit()#提交事务：将当前会话中的所有未提交的更改永久保存到数据库中。结束事务：提交事务后，当前会话中的所有更改将被清除，会话状态将被重置。
        else:
            # 更新session_key
            wechat_user.session_key = session_key#session_key 是会变化的，每次用户重新登录都可能获取新的
            wechat_user.updated_at = datetime.utcnow()
            db.commit()

        # 生成访问令牌
        access_token = create_access_token(wechat_user.user_id)
        
        # 获取用户信息
        user = db.query(User).filter(User.id == wechat_user.user_id).first()
        
        # 构建完整的头像URL
        avatar_url = "http://image.curryking123.online/%E7%9B%B4%E6%8E%A5%E7%BB%99%E9%93%BE%E6%8E%A5/%E5%A4%B4%E5%83%8F%20%E7%94%B7%E5%AD%A9.png"
        # if user.avatar_url:
        #     avatar_url = f"{settings.QINIU_DOMAIN}/{user.avatar_url}"
        
        return {
            "code": 0,
            "data": {
                "username": user.nickname,
                "avatar": avatar_url,
                "token": access_token
            },
            "msg": "登录成功"
        }