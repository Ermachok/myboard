from fastapi import FastAPI

from app.api.v1 import boards, tasks, users
from app.api.v1.users import user_router

app = FastAPI(title="MyBoard API")

app.include_router(user_router)