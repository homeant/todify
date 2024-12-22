from pydantic import BaseModel
from sqlalchemy import BigInteger, Column, Integer, String

from app.core.datastore import Base
from app.utils.date import get_now_millis


class User(Base):
    __tablename__ = "user"

    id = Column(BigInteger, primary_key=True, index=True)
    username = Column(String(50), unique=True, index=True)
    password = Column(String(100))
    nickname = Column(String(80), nullable=False)
    manager = Column(Integer, default=0)  # 0: 普通用户 1：管理员
    status = Column(Integer, default=0)  # 0: 启用 1：禁用
    created_at = Column(BigInteger, default=get_now_millis())
    updated_at = Column(BigInteger, server_onupdate=str(get_now_millis()))


class UserLogin(BaseModel):
    username: str
    password: str


class UserRegister(BaseModel):
    username: str
    password: str
    nickname: str
