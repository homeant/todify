from fastapi import Depends
from sqlalchemy.orm import Session

from app.core.database import get_async_db
from app.user.datastore import UserDatastore
from app.user.service import UserService


def get_user_service(session: Session = Depends(get_async_db)) -> UserService:
    return UserService(UserDatastore(session))
