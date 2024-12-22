# from fastapi import Depends, HTTPException, status
# from fastapi.security import OAuth2PasswordBearer
# from jose import JWTError, jwt
# from app.core.security import SECRET_KEY, ALGORITHM
# from app.user.schemas import TokenData
# from sqlalchemy.orm import Session
# from app.core.basedatastore import get_db
# from app.user.service import UserService
# from app.user.datastore import UserDatastore
#
# oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")
#
# async def get_current_user(
#     token: str = Depends(oauth2_scheme),
#     db: Session = Depends(get_db)
# ):
#     credentials_exception = HTTPException(
#         status_code=status.HTTP_401_UNAUTHORIZED,
#         detail="Could not validate credentials",
#         headers={"WWW-Authenticate": "Bearer"},
#     )
#     try:
#         payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
#         username: str = payload.get("sub")
#         if username is None:
#             raise credentials_exception
#         token_data = TokenData(username=username)
#     except JWTError:
#         raise credentials_exception
#
#     user_service = UserService(UserDatastore(db))
#     user = user_service.datastore.get_user_by_username(username=token_data.username)
#     if user is None:
#         raise credentials_exception
#     return user
