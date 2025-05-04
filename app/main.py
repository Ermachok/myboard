from fastapi import FastAPI

from app.api.v1 import boards, tasks, users

app = FastAPI(title="MyBoard API")
