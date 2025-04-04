from typing import Any
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.api import deps
from app.core.config import settings
from app.core.security import create_access_token
from app.schemas.token import Token
from app.services.wechat_service import WechatService
from app.models.user import User

router = APIRouter()

@router.post("/wechat/login", response_model=Token)
async def wechat_login(
    code: str,
    db: Session = Depends(deps.get_db)
) -> Any:
    """
    微信小程序登录
    """
    try:
        wechat_service = WechatService(
            app_id=settings.WECHAT_APP_ID,
            app_secret=settings.WECHAT_APP_SECRET
        )
        
        # 获取微信用户信息
        wechat_user = await wechat_service.code2session(code)
        
        # 获取或创建用户
        user = wechat_service.get_or_create_user(db, wechat_user)
        
        # 创建访问令牌
        access_token = create_access_token(
            subject=str(user.id),
            expires_delta=settings.WECHAT_TOKEN_EXPIRE_DAYS
        )
        
        return {
            "access_token": access_token,
            "token_type": "bearer",
            "user_info": {
                "id": str(user.id),
                "nickname": user.nickname,
                "avatar": user.avatar
            }
        }
        
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"微信登录失败: {str(e)}"
        )

@router.get("/wechat/userinfo", response_model=dict)
async def get_wechat_user_info(
    current_user: User = Depends(deps.get_current_user)
) -> Any:
    """
    获取当前微信用户信息
    """
    return {
        "id": str(current_user.id),
        "nickname": current_user.nickname,
        "avatar": current_user.avatar
    }