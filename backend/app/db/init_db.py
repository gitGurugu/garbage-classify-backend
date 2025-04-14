import logging
from sqlalchemy.orm import Session
from app.core.config import settings
from app.db.session import engine
from app.models.base import Base
from app.models.user import User
from app.models.wechat_user import WechatUser

logger = logging.getLogger(__name__)

def init_db(db: Session) -> None:
    """
    初始化数据库
    """
    # 创建所有表
    Base.metadata.create_all(bind=engine)
    
    logger.info("数据库表创建完成")
    
    # 检查是否需要创建测试用户（可选）
    test_user = db.query(User).filter(User.nickname == "测试用户").first()
    if not test_user:
        # 创建测试用户
        test_user = User(
            nickname="测试用户"
        )
        db.add(test_user)
        db.flush()
        
        # 创建对应的微信用户记录
        test_wechat_user = WechatUser(
            open_id="test_openid",  # 测试用的openid
            user_id=test_user.id
        )
        db.add(test_wechat_user)
        db.commit()
        logger.info("测试用户已创建")
    else:
        logger.info("测试用户已存在")