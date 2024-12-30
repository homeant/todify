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
    pool_size=20,
    max_overflow=0,
    pool_pre_ping=True,
    pool_recycle=300,
    pool_timeout=3600,
)

# 创建基础模型类
Base = declarative_base()


@contextmanager
def get_db() -> Generator[Session, None, None]:
    session = sessionmaker(bind=engine, expire_on_commit=False)
    with session() as session:
        yield session


@contextmanager
def get_celery_db() -> Generator[Session, None, None]:
    session = sessionmaker(bind=engine, expire_on_commit=False)
    with session() as session:
        yield session


# FastAPI 依赖注入使用的函数
async def get_async_db():
    """
    FastAPI 路由依赖注入使用的数据库会话获取器
    """
    with get_db() as session:
        yield session
