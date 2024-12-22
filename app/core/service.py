from typing import Generic

from typing_extensions import TypeVar

from app.core.datastore import Base, BaseDatastore

D = TypeVar("D", bound=BaseDatastore)
T = TypeVar("T", bound=Base)


class BaseService(Generic[D, T]):
    def __init__(self, datastore: BaseDatastore[T]):
        self.datastore: D = datastore
