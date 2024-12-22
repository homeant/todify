from app.core.execption import BadException
from app.core.security import get_password_hash
from app.core.service import BaseService
from app.user.datastore import UserDatastore
from app.user.schemas import User, UserRegister


class UserService(BaseService[UserDatastore, User]):
    def __init__(self, datastore: UserDatastore):
        super().__init__(datastore)

    def get_user_by_username(self, username) -> User:
        return self.datastore.get_user_by_username(username)

    def user_register(self, register_in: UserRegister) -> User:
        user = self.get_user_by_username(register_in.username)
        if user:
            raise BadException("Username already exists")
        new_user = User(
            username=register_in.username,
            password=get_password_hash(register_in.password),
            nickname=register_in.nickname,
        )
        return self.datastore.upsert(new_user)
