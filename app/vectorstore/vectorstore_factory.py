from app.core.factory import Factory
from app.core.singleton import Singleton
from app.vectorstore._vectorstore import VectorStore


class VectorStoreFactory(Factory[VectorStore], metaclass=Singleton):

    def __init__(self):
        super().__init__(r"class\s+(\w+)\s*\([^)]*VectorStore[^)]*\):")
