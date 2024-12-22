from fastapi import Depends
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.tools.datastore import ToolDatastore
from app.tools.tool_manager import ToolManager


def get_tool_datastore(session: Session = Depends(get_db)) -> ToolDatastore:
    return ToolDatastore(session)


def get_tool_manager(
    datastore: ToolDatastore = Depends(get_tool_datastore),
) -> ToolManager:
    return ToolManager(datastore=datastore)
