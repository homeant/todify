from sqlalchemy import JSON, BigInteger, Column, Integer, String, Text

from app.core.database import Base
from app.utils.date import get_now_millis


class Tool(Base):
    __tablename__ = "tools"

    id = Column(BigInteger, primary_key=True, index=True)
    name = Column(String(255), nullable=True)
    tool_type = Column(String(120), nullable=True)
    function_path = Column(String(200), nullable=True)
    description = Column(Text, nullable=True)
    parameters = Column(JSON, nullable=True)
    status = Column(Integer, default=1)  # 1: 启用 0：禁用
    created_at = Column(BigInteger, default=get_now_millis())
    updated_at = Column(BigInteger, server_onupdate=str(get_now_millis()))
