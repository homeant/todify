import importlib
import inspect
import logging
from typing import Callable, List, Union

import akshare as ak
from langchain.tools import Tool
from pydantic import BaseModel

from app.core.service import BaseService
from app.core.singleton import Singleton
from app.models.tool import Tool as ToolModel
from app.tools.datastore import ToolDatastore
from app.utils.func import format_doc
from app.vectorstore.vectorstore_factory import VectorStoreFactory

logger = logging.getLogger(__name__)

VECTOR_DB_PATH = "tools.db"


class ToolManager(BaseService[ToolDatastore, ToolModel], metaclass=Singleton):
    def __init__(self, datastore: ToolDatastore):
        super().__init__(datastore)
        self._vector_store = VectorStoreFactory().get_instance(
            "QdrantVectorStore", collection_name="tools"
        )
        self._init_tools()

    def _init_tools(self):
        """扫描并保存AKShare工具"""
        try:
            count = self.datastore.get_tools_count_by_type("akshare")
            if count > 0:
                return
            tools = []
            for name, func in inspect.getmembers(ak, inspect.isfunction):
                if name.startswith("_"):
                    continue
                sig = inspect.signature(func)
                tool = ToolModel(
                    name=name,
                    description=format_doc(func),
                    tool_type="akshare",
                    function_path=f"akshare.{name}",
                    parameters={
                        param: (
                            param_info.default
                            if param_info.default != inspect.Parameter.empty
                            else None
                        )
                        for param, param_info in sig.parameters.items()
                    },
                )
                tools.append(tool)
            self.datastore.bulk_save(tools)
            tools = self.datastore.get_tools_by_type("akshare")
            self._save_to_vector_store(tools)
        except Exception as e:
            logger.error(f"扫描AKShare工具失败: {str(e)}")
            raise

    def _save_to_vector_store(self, tools: list[ToolModel]):
        """保存工具到向量数据库"""
        try:
            texts = [f"{tool.name}\n{tool.description}" for tool in tools]
            meta_datas = [
                {
                    "name": tool_config.name,
                    "tool_type": tool_config.tool_type,
                    "function_path": tool_config.function_path,
                }
                for tool_config in tools
            ]
            ids = [tool_config.id for tool_config in tools]
            self._vector_store.add_texts(texts, meta_datas, ids)
        except Exception as e:
            logger.error(f"保存工具到向量数据库失败: {str(e)}")
            raise

    @classmethod
    def _create_tool_function(cls, tool_config: ToolModel) -> Callable:
        """为工具创建包装函数"""

        def wrapper(*args, **kwargs):
            try:
                # 动态导入并调用函数
                logger.info(f"调用工具: {tool_config.name}, 参数: {args}, {kwargs}")
                module_path, func_name = tool_config.function_path.rsplit(".", 1)
                module = importlib.import_module(module_path)
                func = getattr(module, func_name)

                result = func(*args, **kwargs)
                if hasattr(result, "to_markdown"):
                    if len(result) > 100:
                        result = result.head(100)
                    return f"```markdown\n{result.to_markdown(floatfmt=".2f")}\n```"
                return str(result)
            except Exception as e:
                error_msg = f"调用{tool_config.name}时发生错误: {str(e)}"
                logger.error(error_msg)
                return error_msg

        return wrapper

    def search_and_create_tools(
        self, query: Union[str, list[str]], top_k: int = 5
    ) -> List[Tool]:
        """根据用户问题搜索并创建相关工具

        Args:
            query: 用户问题
            top_k: 返回的最相关工具数量

        Returns:
            List[Tool]: 相关工具列表
        """
        try:
            # 使用向量数据库搜索相关工具
            if isinstance(query, str):
                results = self._vector_store.search(query, top_k)
            else:
                results = []
                ids = []
                for q in query:
                    for result in self._vector_store.search(q, top_k):
                        if result.metadata.get("_id") not in ids:
                            results.append(result)
                            ids.append(result.metadata.get("_id"))
            tools = []
            for doc in results:
                # 获取工具配置
                tool_config = self.datastore.get_tool(doc.metadata["_id"])
                if not tool_config:
                    continue
                module_path, func_name = tool_config.function_path.rsplit(".", 1)
                module = importlib.import_module(module_path)
                func = getattr(module, func_name)
                # 创建动态参数模型
                params = inspect.signature(func).parameters
                model_fields = {}
                for name, param in params.items():
                    field_type = param.annotation if param.annotation else str
                    model_fields[name] = field_type

                model_name = f"{tool_config.name}Parameters"
                args_schema = type(
                    model_name,
                    (BaseModel,),
                    {
                        "__annotations__": model_fields,
                    },
                )
                # 创建工具实例
                tool = Tool(
                    name=tool_config.name,
                    description=tool_config.description,
                    func=self._create_tool_function(tool_config),
                    args_schema=args_schema,
                )
                tools.append(tool)

            return tools

        except Exception as e:
            logger.error(f"搜索创建工具失败: {str(e)}")
            return []

    def get_tool(self, tool_type: str, name: str) -> Tool | None:
        """根据工具类型和名称获取工具实例"""
        tool_config = self.datastore.get_tool_by_type_and_name(tool_type, name)
        if tool_config:
            return Tool(
                name=tool_config.name,
                description=tool_config.description,
                func=self._create_tool_function(tool_config),
            )
        return None
