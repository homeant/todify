# 创建数据库引擎
from sqlalchemy import create_engine, QueuePool
from sqlalchemy.orm import declarative_base, sessionmaker

from app.config.setting import settings

engine = create_engine(
    settings.database_url,
    echo=False,
    future=True,
    poolclass=QueuePool,
    pool_size=20,
    max_overflow=0,
    pool_pre_ping=True,
    pool_recycle=300,
    pool_timeout=3600,
)

# 创建会话工厂
SessionLocal = sessionmaker(expire_on_commit=False, bind=engine)

# 创建基础模型类
Base = declarative_base()

def get_db():
    return SessionLocal()

# 获取数据库会话的依赖函数
def get_async_db():
    with SessionLocal() as session:
        yield session