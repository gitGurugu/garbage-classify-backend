from typing import Any

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.schemas.wechat import WeChatCode, WeChatLoginResponse
from app.services.wechat_service import WeChatService

router = APIRouter()

@router.post("/wechat-login", response_model=WeChatLoginResponse, summary="微信登录")
async def wechat_login(
    code: WeChatCode,
    db: Session = Depends(get_db)
) -> Any:
    """
    通过微信小程序登录
    """
    return await WeChatService.login_with_code(db, code.code)
# 校验模型WeChatCode