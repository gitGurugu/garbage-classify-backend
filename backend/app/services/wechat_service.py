# from wechatpy.session.sqlalchemystorage import SQLAlchemyStorage
# from wechatpy.exceptions import WechatError
# from fastapi import HTTPException
# from sqlalchemy.orm import Session
# from typing import Optional
# import httpx
# from pydantic import BaseModel

# from app.core.config import settings 
# from app.models.wechat_user import WechatUser
# from app.models.user import User

# class WechatCode2SessionResponse(BaseModel):
#     openid: str
#     session_key: str
#     unionid: Optional[str] = None
#     errcode: Optional[int] = None
#     errmsg: Optional[str] = None

# class WechatService:
#     def __init__(self, app_id: str, app_secret: str):
#         self.app_id = app_id
#         self.app_secret = app_secret
#         self.code2session_url = "https://api.weixin.qq.com/sns/jscode2session"

#     async def code2session(self, code: str) -> WechatCode2SessionResponse:
#         """
#         通过 code 获取微信用户信息
#         """
#         async with httpx.AsyncClient() as client:
#             params = {
#                 "appid": self.app_id,
#                 "secret": self.app_secret,
#                 "js_code": code,
#                 "grant_type": "authorization_code"
#             }
#             response = await client.get(self.code2session_url, params=params)
#             data = response.json()
            
#             if "errcode" in data and data["errcode"] != 0:
#                 raise HTTPException(
#                     status_code=400,
#                     detail=f"微信登录失败: {data['errmsg']}"
#                 )
                
#             return WechatCode2SessionResponse(**data)

#     def get_or_create_user(
#         self,
#         db: Session,
#         wechat_data: WechatCode2SessionResponse
#     ) -> User:
#         """
#         获取或创建用户
#         """
#         # 查找现有微信用户
#         wechat_user = db.query(WechatUser).filter(
#             WechatUser.openid == wechat_data.openid
#         ).first()
        
#         if wechat_user:
#             return wechat_user.user
            
#         # 创建新用户
#         user = User(
#             nickname=f"微信用户_{wechat_data.openid[:8]}",
#             is_active=True
#         )
#         db.add(user)
#         db.flush()
        
#         # 创建微信用户关联
#         wechat_user = WechatUser(
#             user_id=user.id,
#             openid=wechat_data.openid,
#             unionid=wechat_data.unionid,
#             session_key=wechat_data.session_key
#         )
#         db.add(wechat_user)
#         db.commit()
        
#         return user

# class WechatAuthService:
#     def __init__(self, settings: WechatSettings):
#         self.app_id = settings.WECHAT_APP_ID
#         self.app_secret = settings.WECHAT_APP_SECRET

#     async def login(self, db: Session, code: str):
#         try:
#             # 获取微信登录凭证
#             session_info = await self.code_to_session(code)
            
#             # 获取或创建微信用户
#             wechat_user = self.get_or_create_wechat_user(
#                 db,
#                 open_id=session_info['openid'],
#                 session_key=session_info['session_key']
#             )
            
#             return wechat_user
            
#         except WechatError as e:
#             raise HTTPException(status_code=400, detail=str(e))