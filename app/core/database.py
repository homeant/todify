from contextlib import contextmanager
from typing import Generator
from sqlalchemy import QueuePool, create_engine
from sqlalchemy.orm import declarative_base, sessionmaker, Session
from sqlalchemy.exc import SQLAlchemyError
import logging
from threading import local

from app.config.setting import settings

logger = logging.getLogger(__name__)

# 线程本地存储
thread_local = local()

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

# 创建会话工厂
SessionLocal = sessionmaker(
    expire_on_commit=False,
    bind=engine,
    autocommit=False,
    autoflush=False
)

# 创建基础模型类
Base = declarative_base()

@contextmanager
def get_db() -> Generator[Session, None, None]:
    """
    提供一个数据库会话的上下文管理器
    """
    session = SessionLocal()
    yield session

@contextmanager
def get_celery_db() -> Generator[Session, None, None]:
    """
    专门为 Celery 任务提供的数据库会话上下文管理器
    """
    session = None
    try:
        if not hasattr(thread_local, "session"):
            thread_local.session = SessionLocal()
        session = thread_local.session
        yield session
    finally:
        if session:
            session.close()
            if hasattr(thread_local, "session"):
                delattr(thread_local, "session")

# FastAPI 依赖注入使用的函数
async def get_async_db():
    """
    FastAPI 路由依赖注入使用的数据库会话获取器
    """
    with get_db() as session:
        yield session
