from sqlalchemy import select

from app.core.datastore import BaseDatastore
from app.core.singleton import Singleton
from app.models.tool import Tool


class ToolDatastore(BaseDatastore[Tool], metaclass=Singleton):
    def get_tool(self, primary_id: int) -> Tool:
        return self.db_session.query(Tool).filter(Tool.id == primary_id).first()

    def get_tool_by_type_and_name(self, task_type: str, name: str):
        return (
            self.db_session.query(Tool)
            .filter(Tool.name == name, Tool.status == 1, Tool.tool_type == task_type)
            .first()
        )

    def get_tools_count_by_type(self, tool_type: str) -> int:
        return (
            self.db_session.query(Tool)
            .filter(Tool.tool_type == tool_type, Tool.status == 1)
            .count()
        )

    def get_tools_by_type(self, tool_type: str) -> list[Tool]:
        st = select(Tool).where(Tool.tool_type == tool_type).where(Tool.status == 1)
        return self._fetch_all(st)
