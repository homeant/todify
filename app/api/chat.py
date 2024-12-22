from fastapi import APIRouter, Depends
from fastapi.responses import StreamingResponse

from app.chat.chat_manager import ChatManager
from app.chat.depends import get_chat_manager
from app.chat.schemas import ChatCompletionRequest

router = APIRouter()


@router.post("/completions")
async def chat_completions(
    request: ChatCompletionRequest,
    chat_manager: ChatManager = Depends(get_chat_manager),
):
    """Chat completion API endpoint"""
    response = await chat_manager.handle_completion(request)
    if request.stream:
        return StreamingResponse(
            response,
            media_type="text/event-stream",
            headers={
                "Cache-Control": "no-cache",
                "Connection": "keep-alive",
            },
        )
    return response
