from datetime import timedelta

from fastapi import HTTPException
from starlette import status

from app.auth.schemas import AuthToken
from app.core.security import create_access_token, verify_password
from app.setting import settings
from app.user.schemas import UserLogin
from app.user.service import UserService


class AuthService:
    def __init__(self, user_service: UserService):
        self.user_service = user_service

    def login(self, login_in: UserLogin):
        user = self.user_service.get_user_by_username(login_in.username)
        if not user:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Incorrect username or password",
                headers={"WWW-Authenticate": "Bearer"},
            )
        if not verify_password(login_in.password, user.password):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Incorrect username or password",
                headers={"WWW-Authenticate": "Bearer"},
            )
        access_token_expires = timedelta(seconds=settings.jwt_expire_seconds)
        access_token = create_access_token(
            settings.jwt_secret,
            data={"sub": user.username},
            expires_delta=access_token_expires,
            algorithm=settings.jwt_algorithm,
        )
        return AuthToken(access_token=access_token, token_type="bearer")
