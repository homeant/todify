from fastapi import APIRouter, Depends

from app.user.depends import get_user_service
from app.user.schemas import UserRegister
from app.user.service import UserService

router = APIRouter()


@router.post("/register")
def user_register(
    register_in: UserRegister, user_service: UserService = Depends(get_user_service)
):
    return user_service.user_register(register_in)
