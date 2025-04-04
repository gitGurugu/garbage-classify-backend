from typing import Optional
from pydantic import BaseModel

class WechatCode2SessionResponse(BaseModel):
    openid: str
    session_key: str
    unionid: Optional[str] = None
    errcode: Optional[int] = None
    errmsg: Optional[str] = None