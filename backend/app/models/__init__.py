# 模型包初始化文件

# 首先导入 Base
from app.models.base import Base  # noqa

# 然后导入所有模型，确保它们在SQLAlchemy中注册
from app.models.user import User  # noqa 
from app.models.wechat_user import WechatUser  # noqa
from app.models.garbage_item import GarbageItem
from app.models.history import SearchHistory  # noqa
__all__ = ['Base', 'User', 'WechatUser', 'GarbageItem', 'SearchHistory']
