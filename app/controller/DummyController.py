from http.client import HTTPException

from fastapi import APIRouter

router = APIRouter(
    prefix="/dummy",
    tags=["Dummy"]
)


@router.get("/")
async def get_dummy():
    return {"name": "DummyController 1"}


@router.get("/cool")
async def get_dummy():
    return {"name": "DummyController 2"}