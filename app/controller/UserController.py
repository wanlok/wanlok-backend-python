from typing import Annotated

from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordRequestForm

from app.configs.Security import create_access_token, create_unauthorized_exception, permission, authenticate
from app.model.User import User
from app.services import UserService

router = APIRouter(
    prefix="/user",
    tags=["User"]
)


@router.post("/login")
async def login(form_data: Annotated[OAuth2PasswordRequestForm, Depends()]):
    user = await UserService.get_user_by_username(form_data.username)
    if not authenticate(user, form_data.password):
        raise create_unauthorized_exception("Incorrect username or password")
    return create_access_token(user)


@router.get("/{username}")
async def get(user: Annotated[User, Depends(permission)], username: str):
    return await UserService.get_user_by_username(username)
