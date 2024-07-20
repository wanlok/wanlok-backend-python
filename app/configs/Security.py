from datetime import timedelta, timezone, datetime
from typing import Annotated, Union

import jwt
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jwt import InvalidTokenError
from passlib.context import CryptContext

from app.model.User import User
from app.services import UserService

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# to get a string like this run:
# openssl rand -hex 32
SECRET_KEY = "09d25e094faa6ca2556c818166b7a9563b93f7099f6f0f4caa6cf63b88e8d3e7"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 300


def create_unauthorized_exception(detail: str):
    return HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail=detail,
        headers={"WWW-Authenticate": "Bearer"},
    )


def create_access_token(user: User):
    expiration_time = datetime.now(timezone.utc) + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = jwt.encode({"sub": user.username, "exp": expiration_time}, SECRET_KEY, algorithm=ALGORITHM)
    return {
        # "access_token": access_token,
        # "token_type": "bearer"
        "serviceToken": access_token
    }


async def get_user(token: Annotated[str, Depends(oauth2_scheme)]):
    unauthorized_exception = create_unauthorized_exception("Could not validate credentials")
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise unauthorized_exception
    except InvalidTokenError:
        raise unauthorized_exception
    user = await UserService.get_user_by_username(username)
    if user is None:
        raise unauthorized_exception
    return user


def permission(user: Annotated[User, Depends(get_user)]):
    if user.status.lower() == "disabled":
        raise HTTPException(status_code=400, detail="User disabled")
    return user


def authenticate(user: User, password: str):
    valid = True
    if valid and not user:
        valid = False
    if valid and not pwd_context.verify(password, user.hashed_password):
        valid = False
    return valid
