from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware

from app.controller import DummyController, StudentController, UserController

app = FastAPI()

origins = ["*"]

# * add middleware
app.add_middleware(
    middleware_class=CORSMiddleware,
    allow_origins=origins,
    allow_methods=["*"],
    allow_headers=["*"]
)

app.include_router(DummyController.router)
app.include_router(UserController.router)
app.include_router(StudentController.router)

# if __name__ == "__main__":
