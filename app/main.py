from fastapi import FastAPI
from fastapi.openapi.utils import get_openapi

from app.api.v1.boards import board_router
from app.api.v1.tasks import task_router
from app.api.v1.users import user_router

app = FastAPI(
    title="My board",
    version="1.0.0",
    openapi_tags=[
        {"name": "Users", "description": "Operations with users"},
    ],
)


def custom_openapi():
    if app.openapi_schema:
        return app.openapi_schema
    openapi_schema = get_openapi(
        title="My board",
        version="1.0.0",
        description="API for My board project",
        routes=app.routes,
    )

    openapi_schema["components"]["securitySchemes"] = {
        "BearerAuth": {
            "type": "http",
            "scheme": "bearer",
            "bearerFormat": "JWT",
        }
    }

    for path in openapi_schema["paths"].values():
        for method in path.values():
            if "security" in method:
                method["security"] = [{"BearerAuth": []}]

    app.openapi_schema = openapi_schema
    return app.openapi_schema


app.openapi = custom_openapi
app.include_router(user_router)
app.include_router(board_router)
app.include_router(task_router)
