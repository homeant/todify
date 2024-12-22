from fastapi import APIRouter, Body, Depends

from app.auth.depends import get_auth_service
from app.auth.service import AuthService
from app.user.schemas import UserLogin

router = APIRouter()


@router.post("/login")
def login(
    login_in: UserLogin = Body(...),
    auth_service: AuthService = Depends(get_auth_service),
):
    return auth_service.login(login_in)
