from typing import Optional
from pydantic import BaseModel

class WechatCode2SessionResponse(BaseModel):
    openid: str
    session_key: str
    unionid: Optional[str] = None
    errcode: Optional[int] = None
    errmsg: Optional[str] = None

class WeChatCode(BaseModel):
    code: str
# 前端发送的code
class WeChatLoginResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
    user_id: str