from abc import ABC, abstractmethod
from typing import Iterable, List, Optional, Sequence

from langchain_core.documents import Document


class VectorStore(ABC):

    @abstractmethod
    def add_texts(  # type: ignore
        self,
        texts: Iterable[str],
        meta_datas: Optional[List[dict]] = None,
        ids: Optional[Sequence[str | int]] = None,
    ):
        pass

    def search(self, text: str, k: int = 4) -> List[Document]:
        pass
