from fastapi import FastAPI

from app.controller import DummyController
from app.controller import UserController

app = FastAPI()

app.include_router(DummyController.router)
app.include_router(UserController.router)

# if __name__ == "__main__":
