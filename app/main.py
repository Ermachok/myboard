from fastapi import FastAPI
from fastapi.openapi.utils import get_openapi

from app.api.v1.users import user_router

app = FastAPI(
    title="My board",
    version="1.0.0",
    openapi_tags=[
        {"name": "Users", "description": "Operations with users"},
    ],
)

app.include_router(user_router)


def custom_openapi():
    if app.openapi_schema:
        return app.openapi_schema
    openapi_schema = get_openapi(
        title=app.title,
        version=app.version,
        description="API for My board project",
        routes=app.routes,
    )
    openapi_schema["components"]["securitySchemes"] = {
        "BearerAuth": {
            "type": "http",
            "scheme": "bearer",
            "bearerFormat": "JWT"
        }
    }
    app.openapi_schema = openapi_schema
    return app.openapi_schema


app.openapi = custom_openapi
