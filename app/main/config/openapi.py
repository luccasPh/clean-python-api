from fastapi import FastAPI
from fastapi.openapi.utils import get_openapi


def setup_openapi(app: FastAPI):
    def custom_openapi():
        if app.openapi_schema:
            return app.openapi_schema
        openapi_schema = get_openapi(
            title="Clean Python API",
            version="1.4.0",
            description="API do curso do Mango para realizar enquetes entre programadores",
            routes=app.routes,
            tags=[{"name": "Auth"}, {"name": "Survey"}],
        )
        openapi_schema["paths"]["/api/signup"]["post"]["tags"] = ["Auth"]
        app.openapi_schema = openapi_schema
        return app.openapi_schema

    app.openapi = custom_openapi
