from fastapi import FastAPI

from ..docs.paths import login_path, survey_path, signup_path, survey_result_path
from ..docs.schemas import (
    token_schema,
    login_schema,
    signup_schema,
    error_schema,
    add_survey_schema,
    load_survey_schema,
    save_survey_result_schema,
    load_survey_result_schema,
    api_key_auth_schema,
)
from ..docs.components import bad_request, unauthorized, server_error, forbidden


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
                license=dict(
                    name="MIT License", url="https://opensource.org/licenses/MIT"
                ),
            ),
            tags=[{"name": "Auth"}, {"name": "Survey"}],
            servers=[{"url": "/api"}],
            schemas={
                "token": token_schema,
                "login": login_schema,
                "signup": signup_schema,
                "error": error_schema,
                "add_survey": add_survey_schema,
                "load_survey": load_survey_schema,
                "save_survey_result": save_survey_result_schema,
                "load_survey_result": load_survey_result_schema,
            },
            components={
                "securitySchemes": {"ApiKeyAuth": api_key_auth_schema},
                "bad_request": bad_request,
                "unauthorized": unauthorized,
                "server_error": server_error,
                "forbidden": forbidden,
            },
            paths={
                "/login": login_path,
                "/signup": signup_path,
                "/surveys": survey_path,
                "/surveys/{survey_id}/results": survey_result_path,
            },
        )
        app.openapi_schema = openapi_schema
        return app.openapi_schema

    app.openapi = custom_openapi
