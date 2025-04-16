from typing import Optional
from fastapi import UploadFile
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
class WeChatUserInfo(BaseModel):
    username: str
    avatar: str = ""  # 默认空字符串

class WeChatLoginResponse(BaseModel):
    code: int = 0
    data: dict
    msg: str = "登录成功"

class UpdateUserInfo(BaseModel):
    name: Optional[str] = None
    avatar: Optional[UploadFile] = None