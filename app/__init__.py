from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware

from app.controller import DummyController

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

@app.get("/health")
async def health():
    return {"status": "healthy"}