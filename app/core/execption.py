from fastapi import HTTPException
from starlette import status


class BadException(HTTPException):
    """自定义异常类"""

    def __init__(self, message: str):
        super().__init__(status_code=status.HTTP_400_BAD_REQUEST, detail=message)
