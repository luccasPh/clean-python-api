from fastapi import FastAPI

from ..docs.paths import login_path
from ..docs.schemas import token_schema, login_schema


def setup_openapi(app: FastAPI):
    def custom_openapi():
        if app.openapi_schema:
            return app.openapi_schema
        openapi_schema = dict(
            openapi="3.0.0",
            info=dict(
                title="Clean Python API",
                version="1.0.0",
                description="API do curso do Mango para realizar enquetes entre programadores",
            ),
            tags=[{"name": "Auth"}, {"name": "Survey"}],
            servers=[{"url": "/api"}],
            schemas={"token": token_schema, "login": login_schema},
            paths={"/login": login_path},
        )
        app.openapi_schema = openapi_schema
        return app.openapi_schema

    app.openapi = custom_openapi
