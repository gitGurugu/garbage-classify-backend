from typing import Any, Optional

from fastapi import APIRouter, Depends, UploadFile, File, Form, HTTPException
from sqlalchemy.orm import Session
from qiniu import Auth, put_data

from app.db.session import get_db
from app.schemas.wechat import WeChatCode, WeChatLoginResponse, UpdateUserInfo
from app.services.wechat_service import WeChatService
from app.core.config import settings
from app.utils.deps import get_current_user
from app.models.user import User
from time import time


router = APIRouter()

@router.post("/login-with-wechat", response_model=WeChatLoginResponse, summary="微信登录")
async def wechat_login(
    code: WeChatCode,
    db: Session = Depends(get_db)
) -> Any:
    """
    通过微信小程序登录
    """
    return await WeChatService.login_with_code(db, code.code)

@router.post("/upload-avatar",summary="上传头像")
async def upload_avatar(
    file: UploadFile = File(...),
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    # 初始化七牛云
    q = Auth(settings.QINIU_ACCESS_KEY, settings.QINIU_SECRET_KEY)
    
    # 生成上传token
    token = q.upload_token(settings.QINIU_BUCKET_NAME)
    
    # 读取文件内容
    file_content = await file.read()
    
    # 生成文件名
    file_ext = file.filename.split('.')[-1]
    key = f"avatars/{current_user.id}_{int(time.time())}.{file_ext}"
    
    # 上传到七牛云
    ret, info = put_data(token, key, file_content)
    
    if info.status_code == 200:
        # 更新用户头像
        current_user.avatar_url = key
        db.commit()
        
        return {
            "code": 0,
            "data": {
                "avatar": f"{settings.QINIU_DOMAIN}/{key}"
            },
            "msg": "头像上传成功"
        }
    
    raise HTTPException(status_code=400, detail="头像上传失败")

@router.post("/update",summary="更新用户信息")
async def update_user_info(
    name: Optional[str] = Form(None),
    avatar: Optional[UploadFile] = File(None),
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """修改用户信息"""
    try:
        # 更新名称
        if name:
            current_user.nickname = name

        # 处理头像上传
        if avatar:
            # 初始化七牛云
            q = Auth(settings.QINIU_ACCESS_KEY, settings.QINIU_SECRET_KEY)
            token = q.upload_token(settings.QINIU_BUCKET_NAME)
            
            # 读取文件内容
            file_content = await avatar.read()
            
            # 生成文件名
            file_ext = avatar.filename.split('.')[-1]
            key = f"avatars/{current_user.id}_{int(time.time())}.{file_ext}"
            
            # 上传到七牛云
            ret, info = put_data(token, key, file_content)
            
            if info.status_code != 200:
                raise HTTPException(status_code=400, detail="头像上传失败")
                
            current_user.avatar_url = key

        # 提交更改
        db.commit()
        
        # 构建返回数据
        avatar_url = f"{settings.QINIU_DOMAIN}/{current_user.avatar_url}" if current_user.avatar_url else ""
        
        return {
            "code": 0,
            "data": {
                "username": current_user.nickname,
                "avatar": avatar_url
            },
            "msg": "用户信息更新成功"
        }
        
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=400, detail=f"更新失败: {str(e)}")

@router.get("/user-info", summary="获取用户信息")
async def get_user_info(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """获取当前登录用户信息"""
    try:
        # 构建完整的头像URL
        avatar_url = ""
        if current_user.avatar_url:
            avatar_url = f"{settings.QINIU_DOMAIN}/{current_user.avatar_url}"
            
        return {
            "code": 0,
            "data": {
                "username": current_user.nickname,
                "avatar": avatar_url,
            },
            "msg": "获取用户信息成功"
        }
    except Exception as e:
        return {
            "code": 1,
            "data": {},
            "msg": f"获取用户信息失败: {str(e)}"
        }