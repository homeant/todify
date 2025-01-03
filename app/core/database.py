import logging
from contextlib import contextmanager
from typing import Generator

from sqlalchemy import QueuePool, create_engine
from sqlalchemy.orm import Session, declarative_base, sessionmaker

from app.config.setting import settings

logger = logging.getLogger(__name__)

engine = create_engine(
    settings.database_url,
    echo=True,
    future=True,
    poolclass=QueuePool,
    pool_size=10,  # 最大连接数
    max_overflow=5,  # 额外允许的溢出连接数
    pool_recycle=3600,  # 回收时间，避免长时间空闲连接失效
    pool_pre_ping=True,  # 检测连接是否有效
)

# 创建基础模型类
Base = declarative_base()

SessionLocal = sessionmaker(bind=engine, expire_on_commit=False)

@contextmanager
def get_db() -> Generator[Session, None, None]:
    with SessionLocal() as session:
        yield session


def get_celery_db() -> Session:
    return SessionLocal()


# FastAPI 依赖注入使用的函数
async def get_async_db():
    """
    FastAPI 路由依赖注入使用的数据库会话获取器
    """
    with get_db() as session:
        yield session
