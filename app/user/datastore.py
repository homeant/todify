from sqlalchemy import select

from app.core.datastore import BaseDatastore
from app.user.schemas import User


class UserDatastore(BaseDatastore[User]):
    def get_user_by_username(self, username: str) -> User:
        return self._fetch_one(select(User).where(User.username == username))
