from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.core.config import settings
from app.models.base import Base  # 从 models.base 导入 Base，而不是自己定义

engine = create_engine(settings.SQLALCHEMY_DATABASE_URI, pool_pre_ping=True)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# 依赖项，用于获取数据库会话
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close() 


# 生成器是一种特殊的迭代器，它可以通过 yield 关键字生成一系列值。生成器函数每次调用时，会从上次暂停的地方继续执行，直到遇到下一个 yield 语句。