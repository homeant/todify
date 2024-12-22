from fastapi import Depends

from app.auth.service import AuthService
from app.user.depends import get_user_service
from app.user.service import UserService


def get_auth_service(
    user_service: UserService = Depends(get_user_service),
) -> AuthService:
    return AuthService(user_service)
