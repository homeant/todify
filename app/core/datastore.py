from typing import Generic, TypeVar

from sqlalchemy import Executable
from sqlalchemy.orm import Session

from app.core.database import Base
from app.utils.list import batch_list

# 定义泛型类型变量
T = TypeVar("T", bound=Base)


class BaseDatastore(Generic[T]):
    def __init__(self, db_session: Session):
        self.model = T
        self.db_session = db_session

    def _fetch_one(self, statement: Executable):
        results = self.db_session.execute(statement=statement)
        return results.scalar_one_or_none()

    def _fetch_all(self, statement: Executable, return_dicts: bool = False):
        results = self.db_session.execute(statement=statement)
        if not return_dicts:
            return results.scalars().all()
        else:
            return results.all()

    def upsert(self, instance: T) -> T:
        self.db_session.add(instance)
        self.db_session.commit()
        self.db_session.refresh(instance)
        return instance

    def bulk_save(self, instances: list[T], batch_size: int = 64):
        for items in batch_list(instances, batch_size):
            self.db_session.bulk_save_objects(items)
        self.db_session.commit()

    def _execute(self, statement: Executable):
        self.db_session.execute(statement)
        self.db_session.commit()
