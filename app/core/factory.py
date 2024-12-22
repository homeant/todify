import importlib
import inspect
import os
import re
from typing import Dict, Generic, TypeVar

from app.core.singleton import Singleton

Instance = TypeVar("Instance")


class Factory(Generic[Instance], metaclass=Singleton):

    def __init__(self, pattern: str):
        self.pattern = pattern
        self.classes: Dict[str, str] = {}  # 存储类名和文件名的映射
        self._discover_classes()

    def _discover_classes(self):
        current_dir = os.path.dirname(os.path.abspath(inspect.getfile(self.__class__)))
        pattern = re.compile(self.pattern)
        for filename in os.listdir(current_dir):
            if filename.endswith(".py") and not filename.startswith("_"):
                file_path = os.path.join(current_dir, filename)
                with open(file_path, "r", encoding="utf-8") as file:
                    content = file.read()
                    matches = pattern.findall(content)
                    for class_name in matches:
                        self.classes[class_name] = filename[
                            :-3
                        ]  # 存储类名和模块名的映射

    def get_instance(self, name: str, *args, **kwargs) -> Instance:
        module_name = self.classes.get(name)
        if module_name is None:
            raise ValueError(f"No Embedding implementation found for name: {name}")

        try:
            module = importlib.import_module(
                f".{module_name}", package=inspect.getmodule(self.__class__).__package__
            )
            embedding_class = getattr(module, name)
            return embedding_class(*args, **kwargs)
        except ImportError as e:
            raise ImportError(f"Error importing module {module_name}: {e}")
        except AttributeError:
            raise ValueError(f"Class {name} not found in module {module_name}")
