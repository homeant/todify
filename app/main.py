from fastapi import APIRouter, FastAPI

from app.api.auth import router as auth_router
from app.api.chat import router as chat_router
from app.api.user import router as user_router
from app.core.database import engine
from app.core.datastore import Base
from app.logger import setup_logging

# 创建数据库表
Base.metadata.create_all(bind=engine)


file_path = "./logs/app.log"

setup_logging(file_path)


app = FastAPI()


router = APIRouter(prefix="/api/v1")

router.include_router(auth_router, prefix="/auth")
router.include_router(user_router, prefix="/user")
router.include_router(chat_router, prefix="/chat")

app.include_router(router)


# @app.post("/token")
# async def login_for_access_token(
#     form_data: OAuth2PasswordRequestForm = Depends(),
#     db: Session = Depends(get_db)
# ):
#     user_service = UserService(UserDatastore(db))
#     return user_service.create_user_token(form_data.username, form_data.password)

# @app.get("/users/me/", response_model=schemas.User)
# async def read_users_me(current_user: User = Depends(get_current_user)):
#     return current_user
