from typing import Annotated

from fastapi import APIRouter, Depends

from app.configs.Security import permission
from app.model.User import User

router = APIRouter(
    prefix="/student",
    tags=["Student"]
)


@router.get("/")
def get_students(user: Annotated[User, Depends(permission)],):
    return [
        {
            "name": "Peter Chan",
            "course": "Master of Computer Science"
        },
        {
            "name": "Jack Wong",
            "course": "Master of Information Technology"
        },
        {
            "name": "Tommy Leung",
            "course": "Master of Computer Science"
        }
    ]
