from fastapi import Depends

from app.chat.chat_manager import ChatManager
from app.tools.depends import get_tool_manager
from app.tools.tool_manager import ToolManager


def get_chat_manager(
    tool_manager: ToolManager = Depends(get_tool_manager),
) -> ChatManager:
    return ChatManager(tool_manager=tool_manager)
